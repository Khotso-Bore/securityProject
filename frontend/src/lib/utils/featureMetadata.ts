/**
 * Feature metadata mapping for insider threat detection model
 * Provides human-readable descriptions for each feature
 */
export const featureMetadata: Record<string, string> = {
	// Document destruction
	total_files_burned: 'Total number of files destroyed or deleted',
	burned_from_other: "Files destroyed from other users' accounts",

	// Printing activity
	num_printed_pages_off_hours: 'Pages printed outside normal business hours',
	total_printed_pages: 'Total number of pages printed',

	// Location & access patterns
	num_unique_campus: 'Number of unique campus locations accessed',
	entry_during_weekend: 'Number of system entries or accesses on weekends',
	num_entries: 'Total number of system entries or logins',

	// Risk indicators
	hostility_country_level: 'Geopolitical hostility level of access country',

	// Default fallback
	default: 'Model feature'
};

/**
 * Get human-readable description for a feature
 * @param featureName - The feature name from the model
 * @returns Human-readable description
 */
export function getFeatureDescription(featureName: string): string {
	return featureMetadata[featureName] || featureMetadata['default'];
}
