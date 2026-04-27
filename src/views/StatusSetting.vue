<template>
    <div class="page-shell">
        <section class="page-grid">
            <div class="content-card overflow-hidden">
                <div class="border-b border-white/10 px-6 py-8 md:px-8">
                    <div class="hero-grid items-start">
                        <div class="hero-card">
                            <p class="section-kicker">{{ $t(`BulkSyncLabel`) }}</p>
                            <div class="deco-divider mt-4 lg:mx-0 lg:justify-start">{{ $t(`StatusRecognitionSuite`) }}</div>
                            <h1 class="section-title mt-3">{{ $t(`StatusSetting`) }}</h1>
                            <p class="section-copy mt-4">{{ $t(`statusSettingToolPage`) }}</p>
                            <p class="mt-4 text-sm text-stone-400">{{ $t(`BulkSyncHint`) }}</p>
                        </div>

                        <div class="hero-card">
                            <p class="section-kicker">{{ $t(`StatusActions`) }}</p>
                            <div class="deco-divider mt-4">{{ $t(`StatusControlPanel`) }}</div>
                            <div class="mt-4 grid gap-3 sm:grid-cols-2">
                                <button type="button" class="action-button" @click="openFileUpload()">{{ $t(`Import Setting`) }}</button>
                                <button type="button" class="action-button" @click="download()">{{ $t(`Export Setting`) }}</button>
                                <button type="button" class="action-button action-button--accent" :disabled="syncState.loading" @click="openScreenshotUpload()">
                                    {{ syncState.loading ? $t(`SyncingScreenshots`) : $t(`SyncScreenshots`) }}
                                </button>
                                <button type="button" class="action-button action-button--danger" @click="resetProgress()">{{ $t(`Reset`) }}</button>
                            </div>
                        </div>
                    </div>

                    <input ref="settingsInput" type="file" class="hidden" accept=".txt,.json" @change="handleSettingsUpload">
                    <input ref="screenshotsInput" type="file" class="hidden" accept="image/*" multiple @change="handleScreenshotUpload">

                    <div class="mt-6 grid gap-4 lg:grid-cols-3">
                        <div class="metric-card">
                            <p class="field-label">{{ $t(`ProcessedScreenshots`) }}</p>
                            <p class="deco-stat-value mt-3">{{ syncState.processedScreenshots }}</p>
                        </div>
                        <div class="metric-card">
                            <p class="field-label">{{ $t(`RecognizedEntries`) }}</p>
                            <p class="deco-stat-value mt-3">{{ syncState.recognizedEntries }}</p>
                        </div>
                        <div class="metric-card">
                            <p class="field-label">{{ $t(`LastSyncStatus`) }}</p>
                            <p class="mt-3 text-sm text-stone-300">{{ syncSummary }}</p>
                        </div>
                    </div>

                    <p v-if="syncState.error" class="mt-4 rounded-2xl border border-red-500/40 bg-red-500/10 px-4 py-3 text-sm text-red-100">
                        {{ syncState.error }}
                    </p>
                </div>

                <div class="divide-y divide-white/10">
                    <section v-for="(group, sinnerKey) in All_IDs" :key="sinnerKey" class="px-6 py-8 md:px-8">
                        <div class="flex flex-col gap-8">
                            <div>
                                <p class="section-kicker">{{ $t(`StatusRosterSegment`) }}</p>
                                <div class="deco-divider mt-4 justify-start">{{ $t(`StatusCollection`) }}</div>
                                <h2 class="mt-2 text-2xl font-bold tracking-[0.08em] text-white md:text-3xl">{{ $t(getSinnerName(sinnerKey)) }}</h2>
                            </div>

                            <div>
                                <div class="mb-4 flex items-center justify-between gap-4">
                                    <h3 class="text-lg font-semibold uppercase tracking-[0.18em] text-gold">{{ $t(`Identities`) }}</h3>
                                    <div class="panel-divider flex-1"></div>
                                </div>

                                <div class="deco-list-grid">
                                    <article
                                        v-for="(identity, identityName) in group.IDs"
                                        :key="identityName"
                                        class="muted-panel p-5"
                                    >
                                        <p class="text-xs font-semibold uppercase tracking-[0.22em] text-stone-400">{{ identity.rarity.replace('Rarity', '') }}</p>
                                        <h4 class="mt-3 text-lg font-semibold leading-6 text-white">{{ $t(identityName) }}</h4>

                                        <div class="mt-5 grid gap-3 sm:grid-cols-2">
                                            <label class="block">
                                                <span class="field-label">{{ $t(`uptie`) }}</span>
                                                <select v-model="identity.uptied" class="field-select mt-2" @change="persistProgress()">
                                                    <option value="0">{{ $t(`Don't have`) }}</option>
                                                    <option value="1">{{ $t(`Uptie`) }} 1</option>
                                                    <option value="2">{{ $t(`Uptie`) }} 2</option>
                                                    <option value="3">{{ $t(`Uptie`) }} 3</option>
                                                    <option value="4">{{ $t(`Uptie`) }} 4</option>
                                                </select>
                                            </label>

                                            <label class="block">
                                                <span class="field-label">{{ $t(`level`) }}</span>
                                                <input
                                                    v-model.number="identity.level"
                                                    type="number"
                                                    min="1"
                                                    max="50"
                                                    class="field-select mt-2"
                                                    @change="updateLevel(identity)"
                                                >
                                            </label>
                                        </div>
                                    </article>
                                </div>
                            </div>

                            <div>
                                <div class="mb-4 flex items-center justify-between gap-4">
                                    <h3 class="text-lg font-semibold uppercase tracking-[0.18em] text-gold">{{ $t(`EGO`) }}</h3>
                                    <div class="panel-divider flex-1"></div>
                                </div>

                                <div class="deco-list-grid">
                                    <article
                                        v-for="(ego, egoName) in group.EGOs"
                                        :key="egoName"
                                        class="muted-panel p-5"
                                    >
                                        <p class="text-xs font-semibold uppercase tracking-[0.22em] text-stone-400">{{ ego.rarity.replace('notOriginal', '') }}</p>
                                        <h4 class="mt-3 text-lg font-semibold leading-6 text-white">{{ $t(egoName) }}</h4>

                                        <label class="mt-5 block">
                                            <span class="field-label">{{ $t(`uptie`) }}</span>
                                            <select v-model="ego.uptied" class="field-select mt-2" @change="persistProgress()">
                                                <option value="0">{{ $t(`Don't have`) }}</option>
                                                <option value="1">{{ $t(`Uptie`) }} 1</option>
                                                <option value="2">{{ $t(`Uptie`) }} 2</option>
                                                <option value="3">{{ $t(`Uptie`) }} 3</option>
                                                <option value="4">{{ $t(`Uptie`) }} 4</option>
                                            </select>
                                        </label>
                                    </article>
                                </div>
                            </div>
                        </div>
                    </section>
                </div>
            </div>
        </section>
    </div>
</template>

<script>
import statusdata from '../components/data.js';
import {
    PROGRESS_STORAGE_KEY,
    cloneProgress,
    hydrateProgress,
    mergeRecognizedUpdates,
    sanitizeLevel,
    syncProgressWithScreenshots,
} from '../utils/progressSync';

export default {
    name: 'StatusSetting',
    props: ['StatusData'],
    data() {
        const defaultProgress = statusdata.data().All_IDs;

        return {
            All_IDs: cloneProgress(defaultProgress),
            syncState: {
                loading: false,
                processedScreenshots: 0,
                recognizedEntries: 0,
                matchedNames: [],
                error: '',
                updatedAt: '',
            },
        };
    },
    computed: {
        syncSummary() {
            if (this.syncState.loading) {
                return this.$t('SyncingScreenshots');
            }

            if (this.syncState.error) {
                return this.$t('SyncFailed');
            }

            if (!this.syncState.updatedAt) {
                return this.$t('SyncAwaiting');
            }

            const matchedText = this.syncState.matchedNames.length
                ? this.syncState.matchedNames.slice(0, 3).map((name) => this.$t(name)).join(', ')
                : this.$t('NoMatchesFound');

            return `${this.syncState.updatedAt} · ${matchedText}`;
        },
    },
    methods: {
        createDefaultProgress() {
            return cloneProgress(statusdata.data().All_IDs);
        },
        getSinnerName(itemID) {
            var CorrName;
            switch (itemID) {
                case "YiSangIDs":
                    CorrName = "YiSang";
                    break;
                case "FaustIDs":
                    CorrName = "Faust";
                    break;
                case "DonIDs":
                    CorrName = "Don Quixote";
                    break;
                case "RyoshuIDs":
                    CorrName = "Ryoshu";
                    break;
                case "MeurIDs":
                    CorrName = "Meursault";
                    break;
                case "HongLuIDs":
                    CorrName = "Hong Lu";
                    break;
                case "HeathIDs":
                    CorrName = "Heathcliff";
                    break;
                case "IshIDs":
                    CorrName = "Ishmael";
                    break;
                case "RodionIDs":
                    CorrName = "Rodion";
                    break;
                case "SinclairIDs":
                    CorrName = "Sinclair";
                    break;
                case "OutisIDs":
                    CorrName = "Outis";
                    break;
                case "GregorIDs":
                    CorrName = "Gregor";
                    break;
            }
            return CorrName;
        },
        persistProgress() {
            localStorage.setItem(PROGRESS_STORAGE_KEY, JSON.stringify(this.All_IDs));
        },
        applyProgress(progress) {
            this.All_IDs = hydrateProgress(this.createDefaultProgress(), progress);
            this.persistProgress();
        },
        updateLevel(identity) {
            identity.level = sanitizeLevel(identity.level);
            this.persistProgress();
        },
        download() {
            var type = "text/plain";
            var text = JSON.stringify(this.All_IDs);
            var filename = "StatusSetting.txt";
            // Create an invisible A element
            const a = document.createElement("a");
            a.style.display = "none";
            document.body.appendChild(a);
            // Set the HREF to a Blob representation of the data to be downloaded
            a.href = window.URL.createObjectURL(
                new Blob([text], { type })
            );
            // Use download attribute to set set desired file name
            a.setAttribute("download", filename);
            // Trigger the download by simulating click
            a.click();
            // Cleanup
            window.URL.revokeObjectURL(a.href);
            document.body.removeChild(a);
        },
        openFileUpload() {
            this.$refs.settingsInput.click();
        },
        openScreenshotUpload() {
            this.$refs.screenshotsInput.click();
        },
        async handleSettingsUpload(event) {
            const [file] = event.target.files || [];

            if (!file) {
                return;
            }

            const content = await file.text();
            const parsed = JSON.parse(content);

            this.applyProgress(parsed);
            event.target.value = '';
        },
        async handleScreenshotUpload(event) {
            const files = Array.from(event.target.files || []);

            if (!files.length) {
                return;
            }

            this.syncState = {
                ...this.syncState,
                loading: true,
                error: '',
            };

            try {
                const response = await syncProgressWithScreenshots(files, this.All_IDs);
                const mergedProgress = response.merged_progress
                    ? hydrateProgress(this.createDefaultProgress(), response.merged_progress)
                    : mergeRecognizedUpdates(this.All_IDs, response.updates || []);

                this.applyProgress(mergedProgress);
                this.syncState = {
                    loading: false,
                    processedScreenshots: response.processed_screenshots || files.length,
                    recognizedEntries: (response.updates || []).length,
                    matchedNames: (response.updates || []).map((item) => item.entryKey),
                    error: '',
                    updatedAt: new Date().toLocaleString(),
                };
            } catch (error) {
                this.syncState = {
                    ...this.syncState,
                    loading: false,
                    error: error.message || this.$t('SyncFailed'),
                };
            } finally {
                event.target.value = '';
            }
        },
        restoreProgress() {
            const storedProgress = JSON.parse(localStorage.getItem(PROGRESS_STORAGE_KEY));
            this.All_IDs = hydrateProgress(this.createDefaultProgress(), storedProgress || {});
            this.persistProgress();
        },
        resetProgress() {
            localStorage.removeItem(PROGRESS_STORAGE_KEY);
            this.All_IDs = this.createDefaultProgress();
            this.syncState = {
                loading: false,
                processedScreenshots: 0,
                recognizedEntries: 0,
                matchedNames: [],
                error: '',
                updatedAt: '',
            };
            this.persistProgress();
        },
    },
    mounted() {
        this.restoreProgress();
    },
}
</script>


