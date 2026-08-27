export interface StrategyQuery {
  asset_class?: string|null; instrument?: string|null; strategy_family?: string|null; timeframe?: string|null;
  trade_direction?: "long"|"short"|"both"|null; min_win_rate?: number|null; min_annualized_return?: number|null;
  annualized_return_unit?: "fraction/year"|"money/year"|null; max_drawdown?: number|null;
  max_drawdown_unit?: "fraction"|"money"|null; min_sharpe?: number|null; min_profit_factor?: number|null;
  min_evidence_confidence?: number|null; min_quality_score?: number|null; min_track_record_years?: number|null;
  regime?: string|null; sort?: "quality_score"|"annualized_return"|"win_rate"|"sharpe"|"max_drawdown"; direction?: "asc"|"desc";
}
export interface MetricValue { value:number|null; unit:string; methodology_version:string; evidence_state:"VALID"|"COLLECTING"|"UNAVAILABLE" }
export interface StrategyIntelligenceProfile { schema_version:string; generated_at:string; identity:{strategy_id:string;name:string|null}; classification:{asset_class:string;instruments:string[]}; metrics:Record<string,MetricValue>; evidence:{trade_count:number;confidence:number;quality_state:string}; robustness:Record<string,unknown>; score?:{quality_score:number;components:Record<string,number>} }
export interface IntelligenceSearchResponse { plan:StrategyQuery; items:Array<{profile:StrategyIntelligenceProfile;why_matched:string[];rank_trace:Record<string,unknown>}>; total:number; excluded_total:number; facets:Record<string,Record<string,number>> }
export interface DnaDirectoryClient { interpret(query:string):Promise<{plan:StrategyQuery;confidence:number;clarifications:string[]}>; intelligenceSearch(plan:StrategyQuery):Promise<IntelligenceSearchResponse>; intelligenceCompare(ids:string[]):Promise<unknown>; }
declare global { const DnaDirectoryApi:DnaDirectoryClient }
