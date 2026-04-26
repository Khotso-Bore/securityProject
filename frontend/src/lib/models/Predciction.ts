export interface PredictionResult {
	row_index: number;
	prediction_prob: number;
	is_malicious: boolean;
	feature_contributions: Record<string, number>;
}

export interface Prediction {
	status?: string;
	confidence?: number;
	results?: PredictionResult[];
}
