import os
import glob
import json
import time
import shutil
import ctypes
import re
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict
import copy
from pathlib import Path
from json_layout import configured_product_types, day_dir, iter_day_dirs, load_layout_config, normalize_product_type, product_type_for_product
from paths import BREAKOUT_JSON_ROOT # [V20260510_1945]
from tb_leadership_generator import generate_tb_leadership

try:
	from strategy_predictor import evaluate_pick_now_logic
except ImportError:
	def evaluate_pick_now_logic(features, total_snapshots):
		return (features.get("appearances", 0) >= 20 and features.get("net_trend", 0) > 100 and total_snapshots >= 40)

VERSION = "V20260510_1945" # Path standardization fix
UPDATE_INTERVAL = 5  # Target interval in seconds

def log_debug(msg):
	ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	formatted = f"[{ts}] {msg}"
	try:
		# Use UTF-8 for file writing to prevent crashes on emojis
		with open("summary_gen_debug.log", "a", encoding="utf-8") as f:
			f.write(formatted + "\n")
	except:
		pass

	try:
		# Still try to print, but catch encoding errors for the console
		print(formatted)
	except UnicodeEncodeError:
		# Fallback for non-UTF8 consoles
		print(formatted.encode('ascii', 'replace').decode('ascii'))

def load_json_with_retry(fpath, retries=5):
	for i in range(retries):
		try:
			with open(fpath, 'r') as f:
				return json.load(f)
		except (json.JSONDecodeError, FileNotFoundError, PermissionError):
			time.sleep(0.1)
	return None

def is_process_alive(pid):
	try:
		pid = int(pid)
	except (TypeError, ValueError):
		return False

	if pid <= 0:
		return False

	if os.name == 'nt':
		PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
		kernel32 = ctypes.windll.kernel32
		handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
		if not handle:
			return False
		try:
			exit_code = ctypes.c_ulong()
			if not kernel32.GetExitCodeProcess(handle, ctypes.byref(exit_code)):
				return False
			return exit_code.value == 259  # STILL_ACTIVE
		finally:
			kernel32.CloseHandle(handle)

	try:
		os.kill(pid, 0)
		return True
	except OSError:
		return False

def find_summary_generator_pids():
	script_name = "summary_net_generator.py"
	pids = set()

	if os.name == 'nt':
		try:
			output = subprocess.check_output(
				'wmic process where "name=\'python.exe\'" get CommandLine,ProcessId',
				shell=True,
				text=True,
				encoding='utf-8',
				errors='ignore',
				stderr=subprocess.DEVNULL,
				timeout=5,
			)
			for line in output.splitlines():
				if script_name not in line.lower():
					continue
				match = re.search(r'(\d+)\s*$', line.strip())
				if match:
					try:
						pids.add(int(match.group(1)))
					except ValueError:
						pass
		except Exception:
			return set()
		return pids

	try:
		output = subprocess.check_output(
			["ps", "-eo", "pid=,args="],
			text=True,
			encoding='utf-8',
			errors='ignore',
			stderr=subprocess.DEVNULL,
			timeout=5,
		)
		for line in output.splitlines():
			if script_name not in line.lower():
				continue
			match = re.match(r'\s*(\d+)\s+', line)
			if match:
				try:
					pids.add(int(match.group(1)))
				except ValueError:
					pass
	except Exception:
		return set()
	return pids

def _new_totals():
	return {
		'net': 0.0, 'buy': 0.0, 'sell': 0.0,
		'buy_alt': 0.0, 'sell_alt': 0.0,
		'b_c': 0, 's_c': 0,
		'b_p_c': 0, 's_p_c': 0,
		'live_buy': 0.0, 'live_sell': 0.0
	}

@dataclass(frozen=True)
class TargetContext:
	mode: str
	date_str: str
	target_dir: Path
	product_type: str | None

@dataclass
class TargetState:
	initialized: bool = False
	closed_cache: dict = field(default_factory=lambda: defaultdict(lambda: defaultdict(list)))
	totals: dict = field(default_factory=lambda: defaultdict(lambda: defaultdict(_new_totals)))
	trade_index: list = field(default_factory=list)
	processed_trade_keys: set = field(default_factory=set)

class SummaryGenerator:
	def __init__(self):
		self.base_dir = Path(os.path.dirname(__file__))
		# [V20260510_1945] Use centralized JSON root
		self.json_dir = BREAKOUT_JSON_ROOT
		self.config_path = self.base_dir / "config.json"

		self.processed_files = set()

		# Performance cache: maps fpath -> (mtime, size, last_valid_data)
		self.file_cache = {}

		# Explicit target-scoped state keyed by output directory context.
		self.target_states = {}

	def _target_state_key(self, mode, date_str, target_dir):
		try:
			target_path = Path(target_dir).resolve()
		except Exception:
			target_path = Path(target_dir)
		return f"{str(mode).lower()}|{date_str}|{target_path}"

	def _product_type_for_target_dir(self, mode, date_str, target_dir):
		try:
			target_path = Path(target_dir).resolve()
		except Exception:
			target_path = Path(target_dir)
		mode_root = (self.json_dir / str(mode).lower()).resolve()
		try:
			rel_parts = target_path.relative_to(mode_root).parts
		except Exception:
			return None
		if len(rel_parts) >= 2 and rel_parts[1] == str(date_str):
			return normalize_product_type(rel_parts[0])
		return None

	def _build_target_context(self, mode, date_str, target_dir):
		target_path = Path(target_dir)
		return TargetContext(
			mode=str(mode).lower(),
			date_str=str(date_str),
			target_dir=target_path,
			product_type=self._product_type_for_target_dir(mode, date_str, target_path),
		)

	def _state_for_target(self, context):
		key = self._target_state_key(context.mode, context.date_str, context.target_dir)
		return key, self.target_states.setdefault(key, TargetState())

	def _clear_target_state(self, context):
		key = self._target_state_key(context.mode, context.date_str, context.target_dir)
		self.target_states.pop(key, None)

	def _trade_matches_target_product_type(self, trade_payload, target_product_type):
		if not target_product_type:
			return True
		product = str((trade_payload or {}).get('product') or '').strip().upper()
		if not product:
			return False
		cfg = load_layout_config(self.config_path)
		return product_type_for_product(product, cfg) == target_product_type

	def _hydrate_trade_from_filename(self, fpath, trade_payload):
		payload = dict(trade_payload or {})
		if payload.get('product') and (payload.get('source_strategy') or payload.get('script_name') or payload.get('app_name')):
			if not payload.get('entry_time'):
				filename = os.path.basename(str(fpath or ''))
				match = re.match(
					r"^(?P<strategy>.+?)_(?P<guid>[0-9a-f]{8})_(?P<product>.+?)_(?P<ts>\d{8}_\d{6})_.+?_(?:cld?|op)\.json$",
					filename,
					re.IGNORECASE,
				)
				if match:
					try:
						payload['entry_time'] = datetime.strptime(match.group('ts'), "%Y%m%d_%H%M%S").isoformat()
					except Exception:
						pass
			return payload
		filename = os.path.basename(str(fpath or ''))
		match = re.match(
			r"^(?P<strategy>.+?)_(?P<guid>[0-9a-f]{8})_(?P<product>.+?)_(?P<ts>\d{8}_\d{6})_.+?_(?:cld?|op)\.json$",
			filename,
			re.IGNORECASE,
		)
		if not match:
			return payload
		payload.setdefault('source_strategy', match.group('strategy'))
		payload.setdefault('script_name', match.group('strategy'))
		payload.setdefault('app_name', match.group('strategy'))
		payload.setdefault('product', match.group('product').upper())
		if not payload.get('entry_time'):
			try:
				payload['entry_time'] = datetime.strptime(match.group('ts'), "%Y%m%d_%H%M%S").isoformat()
			except Exception:
				pass
		return payload

	def _closed_path_for_open_file(self, fpath):
		path_str = str(fpath or '')
		if path_str.endswith("_op.json"):
			return path_str[:-8] + "_cld.json"
		if "_open_" in path_str.lower():
			lower = path_str.lower()
			idx = lower.rfind("_open_")
			if idx >= 0:
				return path_str[:idx] + "_closed_" + path_str[idx + len("_open_"):]
		return path_str

	def _normalize_trade_direction(self, trade_payload):
		raw_direction = str((trade_payload or {}).get('direction') or '').strip().upper()
		if raw_direction in ('LONG', 'BUY'):
			return 'LONG'
		if raw_direction in ('SHORT', 'SELL'):
			return 'SHORT'
		for key in ('market_bias_at_open', 'market_bias_latest'):
			bias = str((trade_payload or {}).get(key) or '').strip().upper()
			if bias == 'BUY':
				return 'LONG'
			if bias == 'SELL':
				return 'SHORT'
		return 'LONG'

	def _canonical_trade_strategy(self, fpath, trade_payload):
		payload = trade_payload or {}
		strat = payload.get('source_strategy') or payload.get('script_name') or payload.get('app_name') or 'unknown'
		if not isinstance(strat, str):
			return 'unknown'
		if strat in ('momentum_b_0_tp5.0_sl7.0', 'momentum_s_0_tp5.0_sl7.0'):
			return strat
		if strat in ('momentum', 'momentum_0_tp5.0_sl7.0'):
			direction = self._normalize_trade_direction(payload)
			return 'momentum_b_0_tp5.0_sl7.0' if direction == 'LONG' else 'momentum_s_0_tp5.0_sl7.0'
		return strat

	def _trade_specificity(self, fpath, trade_payload):
		strat = self._canonical_trade_strategy(fpath, trade_payload)
		if strat in ('momentum_b_0_tp5.0_sl7.0', 'momentum_s_0_tp5.0_sl7.0'):
			original = (trade_payload or {}).get('source_strategy') or (trade_payload or {}).get('script_name') or (trade_payload or {}).get('app_name') or ''
			return 2 if original == strat else 1
		if strat and strat != 'unknown':
			return 1
		return 0

	def _trade_dedupe_key(self, fpath, trade_payload, status_hint=None):
		payload = trade_payload or {}
		status = str(status_hint or payload.get('status') or '').upper() or 'UNKNOWN'
		guid = payload.get('guid')
		if guid:
			return f"{status}|guid|{guid}"
		trade_id = payload.get('trade_id')
		if trade_id:
			product = str(payload.get('product') or '').upper()
			direction = str(payload.get('direction') or '').upper()
			entry_time = str(payload.get('entry_time') or payload.get('exit_time') or '')
			return f"{status}|trade_id|{trade_id}|{product}|{direction}|{entry_time}"
		filename = os.path.basename(str(fpath or ''))
		match = re.match(
			r"^(?P<strategy>.+?)_(?P<guid>[0-9a-f]{8})_(?P<product>.+?)_(?P<ts>\d{8}_\d{6})_.+?_(?P<kind>cld?|op)\.json$",
			filename,
			re.IGNORECASE,
		)
		if match:
			return f"{status}|guid|{match.group('guid')}"
		return f"{status}|file|{filename}"

	def _bootstrap_from_preserved_summary(self, state, context):
		preserved_path = context.target_dir / "_summary_net_pre_auto_archive.json"
		if not preserved_path.exists():
			return False

		preserved = load_json_with_retry(preserved_path)
		if not preserved:
			return False

		strategies = preserved.get("strategies")
		if not isinstance(strategies, dict):
			return False

		restored_any = False
		for strat, products in strategies.items():
			if not isinstance(products, dict):
				continue
			for prod, points in products.items():
				if not isinstance(points, list) or not points:
					continue

				closed_points = [copy.deepcopy(pt) for pt in points if not pt.get("open")]
				if not closed_points:
					continue

				state.closed_cache[strat][prod] = closed_points
				last = closed_points[-1]
				stat = state.totals[strat][prod]
				stat['net'] = float(last.get('net', 0.0) or 0.0)
				stat['buy'] = float(last.get('buy_net', 0.0) or 0.0)
				stat['sell'] = float(last.get('sell_net', 0.0) or 0.0)
				stat['buy_alt'] = float(last.get('buy_alt', 0.0) or 0.0)
				stat['sell_alt'] = float(last.get('sell_alt', 0.0) or 0.0)
				stat['b_c'] = int(last.get('b_c', 0) or 0)
				stat['s_c'] = int(last.get('s_c', 0) or 0)
				stat['live_buy'] = float(last.get('live_buy', 0.0) or 0.0)
				stat['live_sell'] = float(last.get('live_sell', 0.0) or 0.0)

				buy_pct = float(last.get('buyPercent', 0.0) or 0.0)
				sell_pct = float(last.get('sellPercent', 0.0) or 0.0)
				stat['b_p_c'] = int(round(stat['b_c'] * buy_pct / 100.0))
				stat['s_p_c'] = int(round(stat['s_c'] * sell_pct / 100.0))
				restored_any = True

		if restored_any:
			log_debug(f"[RESTORE] Bootstrapped {context.mode}/{context.date_str}/{context.product_type or 'default'} from _summary_net_pre_auto_archive.json")
		return restored_any

	def process_trade_dict(self, fpath, t, state, context):
		if not t: return False
		try:
			prod = t.get('product', 'UNKNOWN').upper()
			strat = self._canonical_trade_strategy(fpath, t)
			status = t.get('status', 'OPEN')
			if status != 'CLOSED':
				return False
			trade_key = self._trade_dedupe_key(fpath, t, status_hint='CLOSED')
			if trade_key in state.processed_trade_keys:
				return False
			direction = self._normalize_trade_direction(t)
			is_buy = direction in ('LONG', 'BUY')
			net_pnl = t.get('net_return', 0.0)
			alt_pnl = t.get('alt_net', 0.0)
			is_live = t.get('is_live_trade', False)
			stat = state.totals[strat][prod]
			stat['net'] += net_pnl
			if is_buy:
				stat['buy'] += net_pnl
				stat['buy_alt'] += alt_pnl
				stat['b_c'] += 1
				if net_pnl > 0: stat['b_p_c'] += 1
				if is_live: stat['live_buy'] += net_pnl
			else:
				stat['sell'] += net_pnl
				stat['sell_alt'] += alt_pnl
				stat['s_c'] += 1
				if net_pnl > 0: stat['s_p_c'] += 1
				if is_live: stat['live_sell'] += net_pnl
			time_val = t.get('exit_time') or t.get('entry_time') or datetime.now().isoformat()
			b_pct = round((stat['b_p_c'] / stat['b_c'] * 100), 1) if stat['b_c'] > 0 else 0.0
			s_pct = round((stat['s_p_c'] / stat['s_c'] * 100), 1) if stat['s_c'] > 0 else 0.0
			state.closed_cache[strat][prod].append({
				't': time_val,
				'net': round(stat['net'], 2),
				'buy_net': round(stat['buy'], 2),
				'sell_net': round(stat['sell'], 2),
				'buy_alt': round(stat['buy_alt'], 2),
				'sell_alt': round(stat['sell_alt'], 2),
				'live_buy': round(stat['live_buy'], 2),
				'live_sell': round(stat['live_sell'], 2),
				'b_c': stat['b_c'],
				's_c': stat['s_c'],
				'buyPercent': b_pct,
				'sellPercent': s_pct
			})
			state.trade_index.append({
				'trade_id': t.get('trade_id'),
				'app_name': strat,
				'strategy': t.get('gen_strategy_name') or t.get('strategy') or '',
				'product': prod,
				'direction': direction,
				'status': 'CLOSED',
				'entry_time': t.get('entry_time'),
				'exit_time': t.get('exit_time'),
				'entry_price': t.get('entry_price'),
				'exit_price': t.get('exit_price'),
				'net_return': net_pnl,
				'alt_net': alt_pnl,
				'is_live': is_live,
				'filename': os.path.basename(fpath)
			})
			state.processed_trade_keys.add(trade_key)
			return True
		except Exception as e:
			log_debug(f"Error processing {os.path.basename(fpath)}: {e}")
			return False

	def _get_relevant_json_files(self, target_dir):
		relevant = []
		try:
			with os.scandir(target_dir) as it:
				for entry in it:
					if entry.is_dir():
						relevant.extend(self._get_relevant_json_files(entry.path))
					elif entry.is_file() and entry.name.endswith(".json") and "snapshot" not in entry.name:
						if any(suffix in entry.name for suffix in ("_cl.json", "_cld.json", "_op.json", "_closed_", "_open_")):
							relevant.append(entry.path)
		except Exception as e:
			pass
		return relevant

	def process_date(self, mode, date_str, target_dir):
		context = self._build_target_context(mode, date_str, target_dir)
		target_key, state = self._state_for_target(context)
		json_paths = self._get_relevant_json_files(target_dir)
		if not json_paths:
			if target_key in self.target_states:
				self._clear_target_state(context)
			return
		if not state.initialized:
			log_debug(f"[INIT] Initializing {context.mode}/{context.date_str}/{context.product_type or 'default'} from existing _cld files...")
			cld_paths = [p for p in json_paths if p.endswith("_cld.json") or "_closed_" in p.lower()]
			cld_tuples = []
			for p in cld_paths:
				t = load_json_with_retry(p)
				t = self._hydrate_trade_from_filename(p, t)
				if t and self._trade_matches_target_product_type(t, context.product_type):
					time_v = t.get('exit_time') or t.get('entry_time') or "0"
					cld_tuples.append((time_v, p, t))
			cld_tuples.sort(key=lambda x: (x[0], -self._trade_specificity(x[1], x[2]), os.path.basename(x[1])))
			for _, p, t in cld_tuples:
				self.process_trade_dict(p, t, state, context)
				self.processed_files.add(p)
			if not cld_tuples:
				self._bootstrap_from_preserved_summary(state, context)
			state.initialized = True
		cl_paths = [p for p in json_paths if p.endswith("_cl.json") or ("_closed_" in p.lower() and p not in self.processed_files)]
		new_closures = 0
		cl_tuples = []
		for p in cl_paths:
			if p in self.processed_files: continue
			t = load_json_with_retry(p)
			t = self._hydrate_trade_from_filename(p, t)
			if t and self._trade_matches_target_product_type(t, context.product_type):
				time_v = t.get('exit_time') or t.get('entry_time') or "0"
				cl_tuples.append((time_v, p, t))
		cl_tuples.sort(key=lambda x: (x[0], -self._trade_specificity(x[1], x[2]), os.path.basename(x[1])))
		for _, p, t in cl_tuples:
			if self.process_trade_dict(p, t, state, context):
				self.processed_files.add(p)
				dest = p.replace("_cl.json", "_cld.json")
				try:
					os.rename(p, dest)
					self.processed_files.add(dest)
					new_closures += 1
				except:
					pass
		op_paths = [p for p in json_paths if p.endswith("_op.json") or "_open_" in p.lower()]
		open_data = defaultdict(lambda: defaultdict(list))
		floating_agg = defaultdict(lambda: defaultdict(lambda: {
			'net': 0.0, 'buy_net': 0.0, 'sell_net': 0.0,
			'buy_alt': 0.0, 'sell_alt': 0.0, 'count': 0
		}))
		ephemeral_trades = []
		now_ts = datetime.now().isoformat()
		read_count = 0
		skip_count = 0
		seen_open_trade_keys = set()
		op_tuples = []
		for p in op_paths:
			t = self._hydrate_trade_from_filename(p, load_json_with_retry(p))
			op_tuples.append((p, t, self._trade_specificity(p, t)))
		op_tuples.sort(key=lambda item: (-item[2], os.path.basename(item[0])))
		for p, _, _ in op_tuples:
			try:
				mtime = os.path.getmtime(p)
				size = os.path.getsize(p)
				cache_key = p
				if cache_key in self.file_cache:
					cached_mtime, cached_size, t = self.file_cache[cache_key]
					if mtime == cached_mtime and size == cached_size:
						skip_count += 1
					else:
						t = load_json_with_retry(p)
						self.file_cache[cache_key] = (mtime, size, t)
						read_count += 1
				else:
					t = load_json_with_retry(p)
					self.file_cache[cache_key] = (mtime, size, t)
					read_count += 1
				t = self._hydrate_trade_from_filename(p, t)
				if not t: continue
				if not self._trade_matches_target_product_type(t, context.product_type):
					continue
				payload_status = str(t.get('status') or 'OPEN').upper()
				if payload_status == 'CLOSED':
					if self.process_trade_dict(p, t, state, context):
						self.processed_files.add(p)
						dest = self._closed_path_for_open_file(p)
						if dest != p:
							try:
								os.rename(p, dest)
								self.processed_files.add(dest)
								new_closures += 1
							except:
								pass
					continue
				if payload_status != 'OPEN':
					continue
				trade_key = self._trade_dedupe_key(p, t, status_hint='OPEN')
				if trade_key in seen_open_trade_keys:
					continue
				prod = t.get('product', 'UNKNOWN').upper()
				strat = self._canonical_trade_strategy(p, t)
				direction = self._normalize_trade_direction(t)
				is_buy = direction in ('LONG', 'BUY')
				net_pnl = t.get('net_return', 0.0)
				alt_pnl = t.get('alt_net', 0.0)
				agg = floating_agg[strat][prod]
				agg['net'] += net_pnl
				if is_buy:
					agg['buy_net'] += net_pnl
					agg['buy_alt'] += alt_pnl
				else:
					agg['sell_net'] += net_pnl
					agg['sell_alt'] += alt_pnl
				agg['count'] += 1
				ephemeral_trades.append({
					'trade_id': t.get('trade_id'),
					'app_name': strat,
					'strategy': t.get('strategy', ''),
					'product': prod,
					'direction': direction,
					'status': 'OPEN',
					'entry_time': t.get('entry_time'),
					'entry_price': t.get('entry_price'),
					'net_return': net_pnl,
					'alt_net': alt_pnl,
					'is_live': t.get('is_live_trade', False),
					'filename': os.path.basename(p)
				})
				seen_open_trade_keys.add(trade_key)
			except:
				pass
		for strat, products in floating_agg.items():
			for prod, agg in products.items():
				stat = state.totals[strat][prod]
				open_data[strat][prod].append({
					't': now_ts,
					'net': round(stat['net'] + agg['net'], 2),
					'buy_net': round(stat['buy'] + agg['buy_net'], 2),
					'sell_net': round(stat['sell'] + agg['sell_net'], 2),
					'buy_alt': round(stat['buy_alt'] + agg['buy_alt'], 2),
					'sell_alt': round(stat['sell_alt'] + agg['sell_alt'], 2),
					'live_buy': round(stat['live_buy'], 2),
					'live_sell': round(stat['live_sell'], 2),
					'b_c': stat['b_c'],
					's_c': stat['s_c'],
					'open': True,
					'count': agg['count']
				})
		final_strategies = copy.deepcopy(state.closed_cache)
		for strat, prods in open_data.items():
			for prod, points in prods.items():
				final_strategies[strat][prod].extend(points)
		for strat, prods in final_strategies.items():
			for prod, points in prods.items():
				points.sort(key=lambda x: x.get('t', '0'))
		summary = {
			"last_update": now_ts,
			"session_max_net": 0.0,
			"strategies": final_strategies
		}
		trades_index = {
			"last_update": now_ts,
			"trades": state.trade_index + ephemeral_trades
		}
		top10_history_path = context.target_dir / "_top10_history.json"
		total_snapshots = 0
		appearances_map = defaultdict(int)
		first_net_map = {}
		if top10_history_path.exists():
			try:
				with open(top10_history_path, 'r') as f:
					hdata = json.load(f)
					history = hdata.get("history", [])
					total_snapshots = len(history)
					for snapshot in history:
						for entry in snapshot.get("top10", []):
							sp_key = (entry.get("strategy"), entry.get("product"))
							appearances_map[sp_key] += 1
							if sp_key not in first_net_map:
								first_net_map[sp_key] = entry.get("net", 0.0)
			except Exception as e:
				log_debug(f"[WARN] Failed to load top10 history for pick_now: {e}")
		top_20_candidates = []
		for strat, products in state.totals.items():
			for prod, stat in products.items():
				b_cnt = stat['b_c']
				s_cnt = stat['s_c']
				b_pct = round((stat['b_p_c'] / b_cnt * 100), 1) if b_cnt > 0 else 0.0
				s_pct = round((stat['s_p_c'] / s_cnt * 100), 1) if s_cnt > 0 else 0.0
				sp_key = (strat, prod)
				current_net = round(stat['net'], 2)
				appearances = appearances_map.get(sp_key, 0)
				first_net = first_net_map.get(sp_key, current_net)
				net_trend = current_net - first_net
				features = {
					"appearances": appearances,
					"net_trend": net_trend
				}
				pick_now = evaluate_pick_now_logic(features, total_snapshots)
				top_20_candidates.append({
					"strategy": strat,
					"product": prod,
					"total_net": current_net,
					"buy_net": round(stat['buy'], 2),
					"sell_net": round(stat['sell'], 2),
					"buy_count": b_cnt,
					"sell_count": s_cnt,
					"buyPercent": b_pct,
					"sellPercent": s_pct,
					"trade_count": b_cnt + s_cnt,
					"pick_now": pick_now
				})
		top_20_candidates.sort(key=lambda x: x['total_net'], reverse=True)
		top_20_payload = {
			"last_update": now_ts,
			"top20": top_20_candidates[:200]
		}
		self.atomic_write_json(context.target_dir / "_summary_net.json", summary)
		self.atomic_write_json(context.target_dir / "_trades_summary.json", trades_index)
		self.atomic_write_json(context.target_dir / "_top20.json", top_20_payload)
		if read_count > 0 or new_closures > 0:
			log_debug(
				f"[{context.mode}/{context.product_type or 'default'}/{context.date_str}] "
				f"Updated: {new_closures} new, {read_count} op read ({skip_count} skipped)"
			)

	def atomic_write_json(self, path, data):
		tmp = str(path) + f".{os.getpid()}.tmp"
		try:
			with open(tmp, 'w') as f:
				json.dump(data, f, indent=2)
			for i in range(5):
				try:
					if os.path.exists(path):
						try: os.remove(path)
						except: pass
					os.replace(tmp, str(path))
					break
				except:
					time.sleep(0.1)
		except Exception as e:
			log_debug(f"Write Error {path.name}: {e}")
		finally:
			if os.path.exists(tmp):
				try: os.remove(tmp)
				except: pass

	def run(self):
		log_debug(f"[START] Stateful Summary Generator [{VERSION}]")
		lock_file = self.base_dir / "summary_gen.lock"
		current_pid = os.getpid()
		live_generator_pids = {pid for pid in find_summary_generator_pids() if pid != current_pid}
		if live_generator_pids:
			pid = min(live_generator_pids)
			log_debug(f"[ABORT] Another instance (PID {pid}) is running.")
			return
		if lock_file.exists():
			try:
				pid = int(lock_file.read_text())
				try:
					if is_process_alive(pid):
						log_debug(f"[STALE LOCK] Ignoring live non-generator PID {pid} from summary_gen.lock.")
				except (ValueError, PermissionError):
					pass
			except (ProcessLookupError, ValueError, PermissionError):
				pass
		lock_file.write_text(str(current_pid))
		try:
			while True:
				start_loop = time.time()
				cfg = load_layout_config(self.config_path)
				config_mode = str(cfg.get("run_mode", "live")).lower()
				modes_to_process = [config_mode] if config_mode else ['live', 'sim']
				for mode in modes_to_process:
					date_str = datetime.now().strftime("%Y-%m-%d")
					targets = iter_day_dirs(self.json_dir, mode, date_str, config=cfg)
					if not targets:
						for product_type in configured_product_types(cfg):
							candidate = day_dir(self.json_dir, mode, date_str, product_type)
							if candidate.exists():
								targets.append(candidate)
					for target in targets:
						if target.exists():
							self.process_date(mode, date_str, target)
							try:
								product_type = target.parent.name
								generate_tb_leadership(mode=mode, date_str=date_str, product_type=product_type)
							except: pass
				duration = time.time() - start_loop
				if duration > 1.0:
					log_debug(f"[PERF] Loop took {duration:.2f}s")
				sleep_time = max(0.1, UPDATE_INTERVAL - duration)
				time.sleep(sleep_time)
		except KeyboardInterrupt:
			log_debug("[STOP] Requested by user.")
		except Exception as e:
			log_debug(f"[CRITICAL] {e}")
		finally:
			if lock_file.exists():
				try: os.remove(lock_file)
				except: pass

if __name__ == "__main__":
	SummaryGenerator().run()
