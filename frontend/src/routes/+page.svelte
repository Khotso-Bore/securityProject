<script lang="ts">
	import type { Prediction } from '$lib/models/Predciction';
	import { fade, slide } from 'svelte/transition';

	let file = $state<File | null>(null);
	let isAnalyzing = $state(false);
	let result = $state<Prediction | null>(null);

	function handleFileSelect(e: Event) {
		e.preventDefault();
		const input = e.target as HTMLInputElement;
		const selectedFiles = input.files;

		if (selectedFiles && selectedFiles.length > 0) {
			file = selectedFiles[0];
			console.log(file);
		} else {
			file = null;
		}
	}

	async function submitForAnalysis() {
		console.log('Submitting for analysis');
		//if (!file) return;

		console.log('Submitting for analysis');

		if (!file) return;

		const formData = new FormData();
		formData.append('file', file);

		isAnalyzing = true;
		result = null;

		const response = await fetch('http://127.0.0.1:8000/predict', {
			method: 'POST',
			body: formData
			// Don't set Content-Type header — the browser sets it automatically
			// with the correct multipart boundary
		});

		const data = await response.json();
		const isMalicious = data.prediction;
		//let confidence = response.probability

		result = {
			status: isMalicious ? 'Malicious' : 'Normal',
			confidence: data.probability
		};
		isAnalyzing = false;
	}

	function reset() {
		file = null;
		result = null;
	}
</script>

<svelte:head>
	<title>Insider Threat Detection</title>
	<meta name="description" content="Upload and analyze CSV files for insider threat detection." />
</svelte:head>

<div
	class="flex min-h-screen items-center justify-center bg-gray-900 p-4 text-gray-100 selection:bg-indigo-500/30"
>
	<main
		class="relative w-full max-w-lg overflow-hidden rounded-2xl border border-gray-700 bg-gray-800 p-8 shadow-2xl"
	>
		<header class="mb-10 text-center">
			<span
				class="mb-4 inline-block rounded-full border border-indigo-500/20 bg-indigo-500/10 px-3 py-1 text-xs font-semibold tracking-wider text-indigo-300 uppercase"
			>
				AI Security
			</span>
			<h1
				class="mb-3 bg-gradient-to-r from-gray-100 to-gray-400 bg-clip-text text-3xl font-bold text-transparent"
			>
				Insider Threat Detection
			</h1>
			<p class="text-sm leading-relaxed text-gray-400">
				Upload a user activity CSV log to analyze and identify abnormal behavioral patterns.
			</p>
		</header>

		<div class="space-y-6">
			<div transition:fade={{ duration: 300 }}>
				<div class="mb-6 rounded-xl border border-gray-700 bg-gray-900/50 p-6">
					<label class="mb-2 block text-sm font-medium text-gray-300"> Select CSV Log File </label>
					<input
						type="file"
						accept=".csv"
						on:change={handleFileSelect}
						class="block w-full cursor-pointer text-sm
                                text-gray-400 file:mr-4 file:cursor-pointer
                                file:rounded-lg file:border-0
                                file:bg-gray-700 file:px-4
                                file:py-2 file:text-sm
                                file:font-semibold file:text-gray-200
                                hover:file:bg-gray-600 focus:outline-none"
					/>
					{#if file}
						<div
							class="mt-4 flex items-center justify-between rounded-lg border border-gray-700 bg-gray-800 p-3"
						>
							<div class="mr-4 truncate">
								<p class="truncate text-sm font-medium text-gray-200">{file.name}</p>
								<p class="text-xs text-gray-500">{(file.size / 1024).toFixed(1)} KB</p>
							</div>
							<button
								on:click={() => (file = null)}
								class="rounded px-2 py-1 text-sm font-medium text-red-400 transition-colors hover:bg-red-400/10 hover:text-red-300"
							>
								Remove
							</button>
						</div>
					{/if}
				</div>

				<button
					class="flex w-full items-center justify-center space-x-2 rounded-xl px-4 py-3 font-semibold shadow-lg transition-all {false
						? 'cursor-not-allowed border border-indigo-500/30 bg-indigo-600/50 text-white'
						: 'bg-indigo-600 text-white shadow-indigo-500/25 hover:-translate-y-0.5 hover:bg-indigo-500'}"
					disabled={false}
					on:click={submitForAnalysis}
				>
					{#if isAnalyzing}
						<svg
							class="mr-2 -ml-1 h-5 w-5 animate-spin text-indigo-300"
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 24 24"
						>
							<circle
								class="opacity-25"
								cx="12"
								cy="12"
								r="10"
								stroke="currentColor"
								stroke-width="4"
							></circle>
							<path
								class="opacity-75"
								fill="currentColor"
								d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
							></path>
						</svg>
						<span>Analyzing...</span>
					{:else}
						<span>Submit for Analysis</span>
					{/if}
				</button>
			</div>

			{#if result}
				<div
					class="relative overflow-hidden rounded-xl border bg-gray-900
                        {result.status === 'Malicious'
						? 'border-red-500/50'
						: 'border-emerald-500/50'}"
					transition:slide={{ duration: 400, easing: (t) => --t * t * t + 1 }}
				>
					<div
						class="h-1 w-full {result.status === 'Malicious'
							? 'bg-gradient-to-r from-red-600 to-orange-500'
							: 'bg-gradient-to-r from-emerald-500 to-teal-400'}"
					></div>

					<div class="p-6">
						<div class="mb-6 flex items-start justify-between">
							<h2 class="text-lg font-semibold text-gray-100">Analysis Complete</h2>
							<button
								on:click={reset}
								class="rounded-lg p-1.5 text-gray-400 transition-colors hover:bg-gray-800 hover:text-white"
							>
								<svg
									xmlns="http://www.w3.org/2000/svg"
									width="20"
									height="20"
									viewBox="0 0 24 24"
									fill="none"
									stroke="currentColor"
									stroke-width="2"
									stroke-linecap="round"
									stroke-linejoin="round"
									><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"
									></line></svg
								>
							</button>
						</div>

						<div class="mb-8 flex items-start space-x-4">
							<div
								class="rounded-xl border p-3 {result.status === 'Malicious'
									? 'border-red-500/30 bg-red-500/10 text-red-500'
									: 'border-emerald-500/30 bg-emerald-500/10 text-emerald-400'}"
							>
								{#if result.status === 'Malicious'}
									<svg
										xmlns="http://www.w3.org/2000/svg"
										width="32"
										height="32"
										viewBox="0 0 24 24"
										fill="none"
										stroke="currentColor"
										stroke-width="2"
										stroke-linecap="round"
										stroke-linejoin="round"
									>
										<path
											d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"
										></path>
										<line x1="12" y1="9" x2="12" y2="13"></line>
										<line x1="12" y1="17" x2="12.01" y2="17"></line>
									</svg>
								{:else}
									<svg
										xmlns="http://www.w3.org/2000/svg"
										width="32"
										height="32"
										viewBox="0 0 24 24"
										fill="none"
										stroke="currentColor"
										stroke-width="2"
										stroke-linecap="round"
										stroke-linejoin="round"
									>
										<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
										<polyline points="22 4 12 14.01 9 11.01"></polyline>
									</svg>
								{/if}
							</div>
							<div>
								<h3 class="mb-1 text-xl font-bold text-gray-100">
									<span class={result.status === 'Malicious' ? 'text-red-500' : 'text-emerald-400'}
										>{result.status}</span
									> Activity
								</h3>
								<p class="text-sm leading-relaxed text-gray-400">
									{#if result.status === 'Malicious'}
										Critical anomalies found. Immediate review of user access logs is recommended.
									{:else}
										No significant anomalies detected. Behavioral patterns align with normal
										baselines.
									{/if}
								</p>
							</div>
						</div>

						<div class="mb-6 rounded-xl border border-gray-700/50 bg-black/20 p-4">
							<div class="mb-2 flex items-end justify-between">
								<span class="text-sm font-medium text-gray-400">Confidence Score</span>
								<span
									class="font-mono text-2xl font-bold {result.status === 'Malicious'
										? 'text-red-400'
										: 'text-emerald-400'}">{result.confidence}%</span
								>
							</div>
							<div class="h-2 w-full overflow-hidden rounded-full bg-gray-800">
								<div
									class="h-full rounded-full transition-all duration-1000 ease-out {result.status ===
									'Malicious'
										? 'bg-gradient-to-r from-red-600 to-red-400'
										: 'bg-gradient-to-r from-emerald-600 to-emerald-400'}"
									style="width: {result.confidence}%"
								></div>
							</div>
						</div>

						<div class="flex gap-3">
							<button
								on:click={reset}
								class="flex-1 rounded-lg border border-gray-700 bg-gray-800 px-4 py-2.5 text-sm font-medium transition-colors hover:bg-gray-700"
							>
								Upload New File
							</button>
						</div>
					</div>
				</div>
			{/if}
		</div>
	</main>
</div>
