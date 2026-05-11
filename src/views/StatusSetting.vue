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

                    <div v-if="reviewState.images.length" class="mt-8 border-t border-white/10 pt-8">
                        <div class="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
                            <div>
                                <p class="section-kicker">{{ $t(`RecognitionReview`) }}</p>
                                <div class="deco-divider mt-4 justify-start">{{ $t(`RecognitionWorkspace`) }}</div>
                                <p class="mt-4 max-w-3xl text-sm leading-7 text-stone-300">{{ $t(`RecognitionReviewHint`) }}</p>
                            </div>

                            <div class="grid gap-3 sm:grid-cols-3 xl:min-w-[40rem]">
                                <button type="button" class="action-button" :class="reviewState.manualFrameMode ? 'action-button--accent' : ''" @click="toggleManualFrameMode()">
                                    {{ $t(reviewState.manualFrameMode ? `StopManualFrame` : `StartManualFrame`) }}
                                </button>
                                <button type="button" class="action-button action-button--accent" @click="applyReviewResults()">
                                    {{ $t(`ApplyReviewResults`) }}
                                </button>
                                <button type="button" class="action-button action-button--danger" @click="discardReviewResults()">
                                    {{ $t(`DiscardReviewResults`) }}
                                </button>
                            </div>
                        </div>

                        <div class="mt-6 space-y-6">
                            <article v-for="image in reviewState.images" :key="image.name" class="subtle-panel p-5 md:p-6">
                                <div class="flex flex-col gap-6 xl:grid xl:grid-cols-[minmax(0,1.15fr)_minmax(20rem,0.85fr)] xl:items-start">
                                    <div>
                                        <div class="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
                                            <div>
                                                <p class="field-label">{{ $t(`SourceImage`) }}</p>
                                                <h3 class="mt-2 text-lg font-semibold text-white">{{ image.name }}</h3>
                                            </div>
                                            <p class="text-sm text-stone-400">{{ getReviewCardsForImage(image.name).length }} {{ $t(`RecognizedCards`) }}</p>
                                        </div>

                                        <div
                                            class="relative mt-4 overflow-hidden rounded-[1.5rem] border border-gold/20 bg-black/30"
                                            :class="reviewState.manualFrameMode ? 'cursor-crosshair' : ''"
                                            @pointerdown="beginManualFrame($event, image)"
                                            @pointermove="updateManualFrame($event, image)"
                                            @pointerup="finishManualFrame($event, image)"
                                            @pointercancel="cancelManualFrame()"
                                            @pointerleave="finishManualFrame($event, image)"
                                        >
                                            <img
                                                :src="image.url"
                                                :alt="`${$t('SourceImage')}: ${image.name}`"
                                                class="block h-auto w-full"
                                                @load="handleReviewImageLoad($event, image)"
                                            >

                                            <div class="pointer-events-none absolute inset-0">
                                                <button
                                                    v-for="card in getReviewCardsForImage(image.name)"
                                                    :key="card.id"
                                                    type="button"
                                                    class="pointer-events-auto absolute border-2 shadow-[0_0_18px_rgba(240,197,111,0.16)] transition focus:outline-none"
                                                    :class="[
                                                        card.manual ? 'border-sky-300 bg-sky-400/10' : card.selectedEntryKey ? 'border-gold bg-gold/10' : 'border-red-300 bg-red-400/10',
                                                        isReviewCardSelected(card.id) ? 'ring-2 ring-white/90 ring-offset-2 ring-offset-stone-950' : '',
                                                    ]"
                                                    :style="getReviewBoundsStyle(card.bounds, image)"
                                                    :aria-label="`${$t('MatchedEntry')}: ${card.ocrName || $t('NoDetectedName')}`"
                                                    @click.stop="selectReviewCard(card.id, { scroll: true })"
                                                >
                                                    <span class="absolute left-0 top-0 -translate-y-full rounded-t-md px-2 py-1 text-[0.65rem] font-semibold uppercase tracking-[0.18em] text-stone-950" :class="card.manual ? 'bg-sky-300' : card.selectedEntryKey ? 'bg-gold' : 'bg-red-300'">
                                                        {{ getReviewCardBadge(card) }}
                                                    </span>
                                                </button>

                                                <div
                                                    v-if="reviewState.draft && reviewState.draft.sourceImage === image.name"
                                                    class="absolute border-2 border-dashed border-sky-300 bg-sky-400/10"
                                                    :style="getReviewBoundsStyle(getDraftBounds(), image)"
                                                ></div>
                                            </div>
                                        </div>

                                        <div v-if="reviewState.manualFrameMode" class="mt-4 rounded-2xl border border-sky-300/30 bg-sky-400/10 p-4 text-sm text-sky-100">
                                            <p class="font-semibold uppercase tracking-[0.18em] text-sky-200">{{ $t(`ManualFrameTutorialTitle`) }}</p>
                                            <p class="mt-2 leading-6">{{ $t(`ManualFrameHintActive`) }}</p>
                                        </div>
                                        <p v-else class="mt-3 text-xs leading-6 text-stone-400">{{ $t(`ManualFrameHintIdle`) }}</p>
                                    </div>

                                    <div class="max-h-[42rem] space-y-3 overflow-y-auto pr-1">
                                        <article
                                            v-for="card in getReviewCardsForImage(image.name)"
                                            :key="`${image.name}-${card.id}`"
                                            :ref="(element) => setReviewCardRef(card.id, element)"
                                            class="muted-panel p-4 transition"
                                            :class="isReviewCardSelected(card.id) ? 'ring-2 ring-gold/80 ring-offset-2 ring-offset-stone-950' : ''"
                                            @click="selectReviewCard(card.id)"
                                        >
                                            <div class="flex items-start justify-between gap-4">
                                                <div>
                                                    <p class="field-label">{{ $t(`DetectedName`) }}</p>
                                                    <p class="mt-2 text-sm text-stone-200">{{ card.ocrName || $t(`NoDetectedName`) }}</p>
                                                    <p v-if="card.ocrSupportText && card.ocrSupportText !== card.ocrName" class="mt-2 text-xs leading-5 text-stone-400">
                                                        {{ $t(`DetectedSupportText`) }}: {{ card.ocrSupportText }}
                                                    </p>
                                                </div>
                                                <span class="rounded-full px-3 py-1 text-[0.68rem] font-semibold uppercase tracking-[0.18em]" :class="card.manual ? 'bg-sky-400/15 text-sky-200' : 'bg-gold/15 text-gold'">
                                                    {{ getReviewCardBadge(card) }}
                                                </span>
                                            </div>

                                            <label class="mt-4 block">
                                                <span class="field-label">{{ $t(`ReviewAlias`) }}</span>
                                                <div class="mt-2 flex gap-2">
                                                    <input
                                                        v-model.trim="card.feedbackAlias"
                                                        type="text"
                                                        class="field-select min-w-0 flex-1"
                                                        :placeholder="card.ocrName || $t('NoDetectedName')"
                                                        @change="handleReviewAliasChange(card)"
                                                    >
                                                    <button
                                                        type="button"
                                                        class="action-button action-button--accent min-h-0 px-2 py-1"
                                                        :disabled="!canSaveReviewAlias(card)"
                                                        :title="$t(`SaveHint`)"
                                                        @click.stop="saveReviewAlias(card)"
                                                    >
                                                        <svg class="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                                                            <path d="M5 3h11l3 3v15H5z"></path>
                                                            <path d="M8 3v6h8"></path>
                                                            <path d="M9 14h6"></path>
                                                            <path d="M9 18h6"></path>
                                                        </svg>
                                                        <span class="sr-only">{{ $t(`SaveHint`) }}</span>
                                                    </button>
                                                </div>
                                                <p class="mt-2 text-xs leading-5 text-stone-400">{{ $t(`ReviewAliasHint`) }}</p>
                                                <p v-if="card.feedbackStatus === 'saved'" class="mt-2 text-xs text-emerald-300">{{ $t(`HintSaved`) }}</p>
                                                <p v-else-if="card.feedbackStatus === 'error'" class="mt-2 text-xs text-red-300">{{ card.feedbackError || $t(`FeedbackSaveFailed`) }}</p>
                                            </label>

                                            <div class="mt-4 grid gap-3 sm:grid-cols-2">
                                                <div>
                                                    <p class="field-label">{{ $t(`DetectedConfidence`) }}</p>
                                                    <p class="mt-2 text-sm text-stone-300">{{ formatConfidence(card.confidence) }}</p>
                                                </div>
                                                <div>
                                                    <p class="field-label">{{ $t(`MatchedEntry`) }}</p>
                                                    <select v-model="card.selectedEntryKey" class="field-select mt-2" @change="handleReviewEntryChange(card)">
                                                        <option value="">{{ $t(`NoEntrySelected`) }}</option>
                                                        <optgroup v-for="group in rosterEntryGroups" :key="group.sinnerKey" :label="$t(group.label)">
                                                            <option v-for="entry in group.entries" :key="entry.key" :value="entry.key">
                                                                {{ $t(entry.entryKey) }} · {{ $t(entry.categoryLabel) }}
                                                            </option>
                                                        </optgroup>
                                                    </select>
                                                </div>
                                            </div>

                                            <div class="mt-4 grid gap-3 sm:grid-cols-2">
                                                <label class="block">
                                                    <span class="field-label">{{ $t(`uptie`) }}</span>
                                                    <select v-model="card.uptie" class="field-select mt-2" @change="updateReviewUptie(card)">
                                                        <option value="0">0</option>
                                                        <option value="1">1</option>
                                                        <option value="2">2</option>
                                                        <option value="3">3</option>
                                                        <option value="4">4</option>
                                                    </select>
                                                </label>

                                                <label v-if="reviewCardHasLevel(card)" class="block">
                                                    <span class="field-label">{{ $t(`level`) }}</span>
                                                    <input
                                                        v-model.number="card.level"
                                                        type="number"
                                                        min="1"
                                                        max="50"
                                                        class="field-select mt-2"
                                                        @change="updateReviewLevel(card)"
                                                    >
                                                </label>
                                            </div>

                                            <div class="mt-4 flex justify-end">
                                                <button type="button" class="action-button action-button--danger min-h-0 px-3 py-2 text-xs" @click="removeReviewCard(card.id)">
                                                    {{ $t(`RemoveReviewCard`) }}
                                                </button>
                                            </div>
                                        </article>

                                        <p v-if="!getReviewCardsForImage(image.name).length" class="rounded-2xl border border-white/10 bg-black/20 px-4 py-4 text-sm text-stone-300">
                                            {{ $t(`NoReviewCardsForImage`) }}
                                        </p>
                                    </div>
                                </div>
                            </article>
                        </div>
                    </div>
                </div>

                <div class="divide-y divide-white/10">
                    <section v-for="(group, sinnerKey) in All_IDs" :key="sinnerKey" class="px-6 py-8 md:px-8">
                        <div class="flex flex-col gap-8">
                            <div>

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
                                                <select v-model="identity.uptied" class="field-select mt-2" @change="updateIdentityUptie(identity, identityName)">
                                                    <option v-if="!isLcbSinnerIdentity(identityName)" value="0">{{ $t(`Don't have`) }}</option>
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
                                            <select v-model="ego.uptied" class="field-select mt-2" @change="updateEgoUptie(ego)">
                                                <option v-if="!isOriginalZTierEgo(ego)" value="0">{{ $t(`Don't have`) }}</option>
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
import { nextTick } from 'vue';
import createDefaultRosterProgress from '../components/data.js';
import {
    PROGRESS_STORAGE_KEY,
    cloneProgress,
    hydrateProgress,
    mergeRecognizedUpdates,
    sanitizeLevel,
    sanitizeUptie,
    submitRecognitionFeedback,
    syncProgressWithScreenshots,
} from '../utils/progressSync';

const REVIEW_DB_NAME = 'dante-review-cache';
const REVIEW_STORE_NAME = 'pending-review';
const REVIEW_CACHE_KEY = 'status-setting';

function openReviewDatabase() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open(REVIEW_DB_NAME, 1);

        request.onupgradeneeded = () => {
            const database = request.result;

            if (!database.objectStoreNames.contains(REVIEW_STORE_NAME)) {
                database.createObjectStore(REVIEW_STORE_NAME);
            }
        };

        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error || new Error('Failed to open review cache'));
    });
}

async function readPendingReviewCache() {
    const database = await openReviewDatabase();

    return new Promise((resolve, reject) => {
        const transaction = database.transaction(REVIEW_STORE_NAME, 'readonly');
        const store = transaction.objectStore(REVIEW_STORE_NAME);
        const request = store.get(REVIEW_CACHE_KEY);

        request.onsuccess = () => resolve(request.result || null);
        request.onerror = () => reject(request.error || new Error('Failed to read review cache'));
        transaction.oncomplete = () => database.close();
        transaction.onerror = () => reject(transaction.error || new Error('Failed to read review cache'));
    });
}

async function writePendingReviewCache(payload) {
    const database = await openReviewDatabase();

    return new Promise((resolve, reject) => {
        const transaction = database.transaction(REVIEW_STORE_NAME, 'readwrite');
        const store = transaction.objectStore(REVIEW_STORE_NAME);

        store.put(payload, REVIEW_CACHE_KEY);
        transaction.oncomplete = () => {
            database.close();
            resolve();
        };
        transaction.onerror = () => reject(transaction.error || new Error('Failed to write review cache'));
    });
}

async function clearPendingReviewCache() {
    const database = await openReviewDatabase();

    return new Promise((resolve, reject) => {
        const transaction = database.transaction(REVIEW_STORE_NAME, 'readwrite');
        const store = transaction.objectStore(REVIEW_STORE_NAME);

        store.delete(REVIEW_CACHE_KEY);
        transaction.oncomplete = () => {
            database.close();
            resolve();
        };
        transaction.onerror = () => reject(transaction.error || new Error('Failed to clear review cache'));
    });
}

export default {
    name: 'StatusSetting',
    props: ['StatusData'],
    data() {
        const defaultProgress = hydrateProgress(createDefaultRosterProgress(), {});

        return {
            All_IDs: cloneProgress(defaultProgress),
            syncState: {
                loading: false,
                processedScreenshots: 0,
                recognizedEntries: 0,
                matchedNames: [],
                error: '',
                updatedAt: '',
                reviewPending: false,
            },
            reviewState: {
                images: [],
                cards: [],
                manualFrameMode: false,
                draft: null,
                nextCardId: 1,
                selectedCardId: null,
            },
            reviewCardRefs: {},
            reviewPersistenceReady: false,
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

            if (this.syncState.reviewPending) {
                return `${this.syncState.updatedAt} · ${this.$t('ReviewPending')}`;
            }

            const matchedText = this.syncState.matchedNames.length
                ? this.syncState.matchedNames.slice(0, 3).map((name) => this.$t(name)).join(', ')
                : this.$t('NoMatchesFound');

            return `${this.syncState.updatedAt} · ${matchedText}`;
        },
        rosterEntryGroups() {
            return Object.entries(this.createDefaultProgress()).map(([sinnerKey, sinnerGroup]) => ({
                sinnerKey,
                label: this.getSinnerName(sinnerKey),
                entries: [
                    ...Object.keys(sinnerGroup.IDs).map((entryKey) => ({
                        key: this.serializeEntryKey({ sinnerKey, category: 'IDs', entryKey }),
                        sinnerKey,
                        category: 'IDs',
                        entryKey,
                        categoryLabel: 'Identities',
                    })),
                    ...Object.keys(sinnerGroup.EGOs).map((entryKey) => ({
                        key: this.serializeEntryKey({ sinnerKey, category: 'EGOs', entryKey }),
                        sinnerKey,
                        category: 'EGOs',
                        entryKey,
                        categoryLabel: 'EGO',
                    })),
                ],
            }));
        },
    },
    methods: {
        createDefaultProgress() {
            return hydrateProgress(createDefaultRosterProgress(), {});
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
        serializeEntryKey({ sinnerKey, category, entryKey }) {
            return `${sinnerKey}::${category}::${entryKey}`;
        },
        parseEntryKey(value) {
            if (!value) {
                return null;
            }

            const [sinnerKey, category, ...entryParts] = value.split('::');

            if (!sinnerKey || !category || !entryParts.length) {
                return null;
            }

            return {
                sinnerKey,
                category,
                entryKey: entryParts.join('::'),
                hasLevel: category === 'IDs',
            };
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
        isLcbSinnerIdentity(identityName) {
            return typeof identityName === 'string' && identityName.startsWith('LCB Sinner');
        },
        isOriginalZTierEgo(ego) {
            return ego?.rarity === 'Z';
        },
        updateIdentityUptie(identity, identityName) {
            const minimumUptie = this.isLcbSinnerIdentity(identityName) ? 1 : 0;
            identity.uptied = String(Math.max(minimumUptie, Number.parseInt(identity.uptied, 10) || 0));
            this.persistProgress();
        },
        updateEgoUptie(ego) {
            const minimumUptie = this.isOriginalZTierEgo(ego) ? 1 : 0;
            ego.uptied = String(Math.max(minimumUptie, Number.parseInt(ego.uptied, 10) || 0));
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
        clearReviewImages() {
            this.reviewState.images.forEach((image) => {
                if (image.url) {
                    URL.revokeObjectURL(image.url);
                }
            });
        },
        resetReviewState() {
            this.clearReviewImages();
            this.reviewCardRefs = {};
            this.reviewState = {
                images: [],
                cards: [],
                manualFrameMode: false,
                draft: null,
                nextCardId: 1,
                selectedCardId: null,
            };
        },
        buildReviewImages(files) {
            return files.map((file) => ({
                name: file.name,
                url: URL.createObjectURL(file),
                naturalWidth: 0,
                naturalHeight: 0,
                file,
            }));
        },
        createReviewCard(rawCard = {}) {
            const matchedEntry = rawCard.matched_entry || rawCard.matchedEntry || null;
            const ocrName = rawCard.ocr_name || rawCard.ocrName || '';
            const rawOcrName = rawCard.raw_ocr_name || rawCard.rawOcrName || ocrName;
            const ocrSupportText = rawCard.ocr_support_text || rawCard.ocrSupportText || '';
            const ocrSinnerHint = rawCard.ocr_sinner_hint || rawCard.ocrSinnerHint || '';

            return {
                id: this.reviewState.nextCardId++,
                sourceImage: rawCard.source_image || rawCard.sourceImage || '',
                bounds: rawCard.bounds || { x: 0, y: 0, width: 0, height: 0 },
                ocrName,
                rawOcrName,
                ocrSupportText,
                ocrSinnerHint,
                feedbackAlias: rawCard.feedbackAlias || ocrName,
                feedbackStatus: rawCard.feedbackStatus || 'idle',
                feedbackError: rawCard.feedbackError || '',
                confidence: Number(rawCard.confidence || 0),
                selectedEntryKey: matchedEntry ? this.serializeEntryKey(matchedEntry) : '',
                uptie: sanitizeUptie(rawCard.uptie ?? rawCard.uptied ?? 0),
                level: sanitizeLevel(rawCard.level ?? 1),
                manual: Boolean(rawCard.manual),
            };
        },
        getReviewCardsForImage(sourceImage) {
            return this.reviewState.cards.filter((card) => card.sourceImage === sourceImage);
        },
        isReviewCardSelected(cardId) {
            return this.reviewState.selectedCardId === cardId;
        },
        handleReviewImageLoad(event, image) {
            image.naturalWidth = event.target.naturalWidth;
            image.naturalHeight = event.target.naturalHeight;
        },
        getReviewBoundsStyle(bounds, image) {
            if (!image.naturalWidth || !image.naturalHeight) {
                return { display: 'none' };
            }

            return {
                left: `${(bounds.x / image.naturalWidth) * 100}%`,
                top: `${(bounds.y / image.naturalHeight) * 100}%`,
                width: `${(bounds.width / image.naturalWidth) * 100}%`,
                height: `${(bounds.height / image.naturalHeight) * 100}%`,
            };
        },
        getReviewCardBadge(card) {
            if (card.manual) {
                return this.$t('ManualCard');
            }

            if (!card.selectedEntryKey) {
                return this.$t('UnmatchedCard');
            }

            return this.$t('AutoDetectedCard');
        },
        reviewCardHasLevel(card) {
            return this.parseEntryKey(card.selectedEntryKey)?.hasLevel || false;
        },
        formatConfidence(value) {
            return `${Math.round(Number(value || 0) * 100)}%`;
        },
        setReviewCardRef(cardId, element) {
            if (element) {
                this.reviewCardRefs[cardId] = element;
                return;
            }

            delete this.reviewCardRefs[cardId];
        },
        async selectReviewCard(cardId, options = {}) {
            const { scroll = false } = options;
            this.reviewState.selectedCardId = cardId;

            if (!scroll) {
                this.persistPendingReview();
                return;
            }

            await nextTick();
            const element = this.reviewCardRefs[cardId];

            if (element?.scrollIntoView) {
                element.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }

            this.persistPendingReview();
        },
        handleReviewEntryChange(card) {
            const entry = this.parseEntryKey(card.selectedEntryKey);
            card.feedbackStatus = 'idle';
            card.feedbackError = '';

            if (!entry) {
                card.level = sanitizeLevel(card.level ?? 1);
                this.persistPendingReview();
                return;
            }

            if (!entry.hasLevel) {
                card.level = 1;
            } else {
                card.level = sanitizeLevel(card.level);
            }

            this.persistPendingReview();
        },
        handleReviewAliasChange(card) {
            card.feedbackAlias = String(card.feedbackAlias || '').trim();
            card.feedbackStatus = 'idle';
            card.feedbackError = '';
            this.persistPendingReview();
        },
        canSaveReviewAlias(card) {
            return Boolean(this.parseEntryKey(card.selectedEntryKey) && String(card.feedbackAlias || '').trim() && card.feedbackStatus !== 'saving');
        },
        getReviewImageBlob(sourceImage) {
            return this.reviewState.images.find((image) => image.name === sourceImage)?.file || null;
        },
        async cropReviewCardDataUrl(card) {
            const imageBlob = this.getReviewImageBlob(card.sourceImage);
            if (!(imageBlob instanceof Blob) || !card?.bounds) {
                return '';
            }

            const cropBounds = {
                x: Math.max(0, Math.round(Number(card.bounds.x || 0))),
                y: Math.max(0, Math.round(Number(card.bounds.y || 0))),
                width: Math.max(1, Math.round(Number(card.bounds.width || 0))),
                height: Math.max(1, Math.round(Number(card.bounds.height || 0))),
            };

            if (typeof createImageBitmap === 'function') {
                const bitmap = await createImageBitmap(imageBlob);

                try {
                    const width = Math.max(1, Math.min(cropBounds.width, bitmap.width - cropBounds.x));
                    const height = Math.max(1, Math.min(cropBounds.height, bitmap.height - cropBounds.y));
                    const canvas = document.createElement('canvas');
                    const context = canvas.getContext('2d');

                    if (!context) {
                        return '';
                    }

                    canvas.width = width;
                    canvas.height = height;
                    context.drawImage(bitmap, cropBounds.x, cropBounds.y, width, height, 0, 0, width, height);
                    return canvas.toDataURL('image/png');
                } finally {
                    if (typeof bitmap.close === 'function') {
                        bitmap.close();
                    }
                }
            }

            return '';
        },
        async buildRecognitionFeedbackItem(card) {
            const entry = this.parseEntryKey(card.selectedEntryKey);

            if (!entry) {
                return null;
            }

            const feedbackAlias = String(card.feedbackAlias || '').trim();
            const detectedName = String(card.ocrName || '').trim();
            const correctedText = feedbackAlias && feedbackAlias !== detectedName
                ? feedbackAlias
                : entry.entryKey;

            return {
                entry,
                corrected_text: correctedText,
                observed_name: feedbackAlias || detectedName,
                raw_ocr_name: String(card.rawOcrName || card.ocrName || '').trim(),
                ocr_support_text: String(card.ocrSupportText || '').trim(),
                ocr_sinner_hint: String(card.ocrSinnerHint || '').trim(),
                recognition_confidence: Number(card.confidence || 0),
                card_image_data_url: await this.cropReviewCardDataUrl(card),
                source_image: String(card.sourceImage || ''),
                bounds: {
                    x: Number(card.bounds?.x || 0),
                    y: Number(card.bounds?.y || 0),
                    width: Number(card.bounds?.width || 0),
                    height: Number(card.bounds?.height || 0),
                },
                manual: Boolean(card.manual),
            };
        },
        async saveReviewAlias(card) {
            const entry = this.parseEntryKey(card.selectedEntryKey);

            if (!entry) {
                card.feedbackStatus = 'error';
                card.feedbackError = this.$t('SelectEntryBeforeSavingHint');
                this.persistPendingReview();
                return;
            }

            card.feedbackStatus = 'saving';
            card.feedbackError = '';
            this.persistPendingReview();

            try {
                const feedbackItem = await this.buildRecognitionFeedbackItem(card);

                if (!feedbackItem?.card_image_data_url) {
                    throw new Error(this.$t('FeedbackSaveFailed'));
                }

                await submitRecognitionFeedback([feedbackItem]);
                card.feedbackStatus = 'saved';
            } catch (error) {
                card.feedbackStatus = 'error';
                card.feedbackError = error.message || this.$t('FeedbackSaveFailed');
            }

            this.persistPendingReview();
        },
        updateReviewUptie(card) {
            card.uptie = sanitizeUptie(card.uptie);
            this.persistPendingReview();
        },
        updateReviewLevel(card) {
            card.level = sanitizeLevel(card.level);
            this.persistPendingReview();
        },
        removeReviewCard(cardId) {
            this.reviewState.cards = this.reviewState.cards.filter((card) => card.id !== cardId);

            if (this.reviewState.selectedCardId === cardId) {
                this.reviewState.selectedCardId = this.reviewState.cards[0]?.id || null;
            }

            this.persistPendingReview();
        },
        toggleManualFrameMode() {
            this.reviewState.manualFrameMode = !this.reviewState.manualFrameMode;
            this.reviewState.draft = null;
            this.persistPendingReview();
        },
        getPointerBounds(event, image) {
            const rect = event.currentTarget.getBoundingClientRect();
            const offsetX = Math.min(Math.max(event.clientX - rect.left, 0), rect.width);
            const offsetY = Math.min(Math.max(event.clientY - rect.top, 0), rect.height);

            return {
                x: (offsetX / rect.width) * image.naturalWidth,
                y: (offsetY / rect.height) * image.naturalHeight,
            };
        },
        beginManualFrame(event, image) {
            if (!this.reviewState.manualFrameMode || !image.naturalWidth || !image.naturalHeight) {
                return;
            }

            const point = this.getPointerBounds(event, image);
            this.reviewState.draft = {
                sourceImage: image.name,
                startX: point.x,
                startY: point.y,
                currentX: point.x,
                currentY: point.y,
            };

            if (event.currentTarget.setPointerCapture) {
                event.currentTarget.setPointerCapture(event.pointerId);
            }
        },
        updateManualFrame(event, image) {
            if (!this.reviewState.draft || this.reviewState.draft.sourceImage !== image.name) {
                return;
            }

            const point = this.getPointerBounds(event, image);
            this.reviewState.draft.currentX = point.x;
            this.reviewState.draft.currentY = point.y;
        },
        getDraftBounds() {
            const draft = this.reviewState.draft;

            if (!draft) {
                return { x: 0, y: 0, width: 0, height: 0 };
            }

            return {
                x: Math.min(draft.startX, draft.currentX),
                y: Math.min(draft.startY, draft.currentY),
                width: Math.abs(draft.currentX - draft.startX),
                height: Math.abs(draft.currentY - draft.startY),
            };
        },
        finishManualFrame(event, image) {
            if (!this.reviewState.draft || this.reviewState.draft.sourceImage !== image.name) {
                return;
            }

            if (event?.type === 'pointerleave' && event.buttons === 1) {
                return;
            }

            this.updateManualFrame(event, image);
            const bounds = this.getDraftBounds();

            if (bounds.width >= 20 && bounds.height >= 20) {
                this.reviewState.cards.push(
                    this.createReviewCard({
                        source_image: image.name,
                        bounds,
                        ocr_name: '',
                        level: 1,
                        uptie: 1,
                        confidence: 1,
                        manual: true,
                    })
                );

                const createdCard = this.reviewState.cards[this.reviewState.cards.length - 1];
                this.selectReviewCard(createdCard.id, { scroll: true });
            } else {
                this.persistPendingReview();
            }

            this.reviewState.draft = null;
        },
        cancelManualFrame() {
            this.reviewState.draft = null;
        },
        serializePendingReview() {
            if (!this.reviewState.images.length) {
                return null;
            }

            return {
                syncState: {
                    processedScreenshots: this.syncState.processedScreenshots,
                    recognizedEntries: this.syncState.recognizedEntries,
                    matchedNames: Array.from(this.syncState.matchedNames || []),
                    error: this.syncState.error,
                    updatedAt: this.syncState.updatedAt,
                    reviewPending: this.syncState.reviewPending,
                },
                reviewState: {
                    cards: this.reviewState.cards.map((card) => ({
                        id: card.id,
                        sourceImage: card.sourceImage,
                        bounds: {
                            x: Number(card.bounds?.x || 0),
                            y: Number(card.bounds?.y || 0),
                            width: Number(card.bounds?.width || 0),
                            height: Number(card.bounds?.height || 0),
                        },
                        ocrName: card.ocrName,
                        rawOcrName: card.rawOcrName,
                        ocrSupportText: card.ocrSupportText,
                        ocrSinnerHint: card.ocrSinnerHint,
                        feedbackAlias: card.feedbackAlias,
                        feedbackStatus: card.feedbackStatus,
                        feedbackError: card.feedbackError,
                        confidence: card.confidence,
                        selectedEntryKey: card.selectedEntryKey,
                        uptie: card.uptie,
                        level: card.level,
                        manual: card.manual,
                    })),
                    manualFrameMode: this.reviewState.manualFrameMode,
                    nextCardId: this.reviewState.nextCardId,
                    selectedCardId: this.reviewState.selectedCardId,
                },
                images: this.reviewState.images
                    .filter((image) => image.file instanceof Blob)
                    .map((image) => ({
                        name: String(image.name || ''),
                        file: image.file,
                    })),
            };
        },
        async persistPendingReview() {
            if (!this.reviewPersistenceReady) {
                return;
            }

            const snapshot = this.serializePendingReview();

            try {
                if (!snapshot || !this.syncState.reviewPending) {
                    await clearPendingReviewCache();
                    return;
                }

                await writePendingReviewCache(snapshot);
            } catch (error) {
                console.error('Failed to persist review state', error);
            }
        },
        async restorePendingReview() {
            try {
                const cached = await readPendingReviewCache();

                if (!cached?.images?.length || !cached?.reviewState) {
                    return;
                }

                this.resetReviewState();
                this.reviewState.images = this.buildReviewImages(cached.images.map((image) => image.file));
                this.reviewState.images.forEach((image, index) => {
                    image.name = cached.images[index]?.name || image.name;
                });
                this.reviewState.cards = (cached.reviewState.cards || []).map((card) => this.createReviewCard(card));
                this.reviewState.manualFrameMode = Boolean(cached.reviewState.manualFrameMode);
                this.reviewState.nextCardId = Math.max(
                    Number(cached.reviewState.nextCardId || 1),
                    this.reviewState.cards.reduce((maxId, card) => Math.max(maxId, Number(card.id || 0)), 0) + 1
                );
                this.reviewState.selectedCardId = cached.reviewState.selectedCardId || this.reviewState.cards[0]?.id || null;
                this.syncState = {
                    ...this.syncState,
                    loading: false,
                    processedScreenshots: cached.syncState?.processedScreenshots || 0,
                    recognizedEntries: cached.syncState?.recognizedEntries || this.reviewState.cards.length,
                    matchedNames: cached.syncState?.matchedNames || [],
                    error: cached.syncState?.error || '',
                    updatedAt: cached.syncState?.updatedAt || '',
                    reviewPending: Boolean(cached.syncState?.reviewPending),
                };
            } catch (error) {
                console.error('Failed to restore review state', error);
            }
        },
        buildReviewUpdates() {
            const deduped = new Map();

            this.reviewState.cards.forEach((card) => {
                const entry = this.parseEntryKey(card.selectedEntryKey);

                if (!entry) {
                    return;
                }

                const key = this.serializeEntryKey(entry);
                const candidate = {
                    sinnerKey: entry.sinnerKey,
                    category: entry.category,
                    entryKey: entry.entryKey,
                    uptied: sanitizeUptie(card.uptie),
                    level: entry.hasLevel ? sanitizeLevel(card.level) : null,
                    confidence: Number(card.confidence || 0),
                    manual: card.manual,
                };

                const existing = deduped.get(key);
                if (!existing || candidate.manual || candidate.confidence >= existing.confidence) {
                    deduped.set(key, candidate);
                }
            });

            return Array.from(deduped.values());
        },
        async applyReviewResults() {
            const updates = this.buildReviewUpdates();
            const mergedProgress = mergeRecognizedUpdates(this.All_IDs, updates);

            this.applyProgress(mergedProgress);
            this.syncState = {
                ...this.syncState,
                recognizedEntries: updates.length,
                matchedNames: updates.map((item) => item.entryKey),
                error: '',
                updatedAt: new Date().toLocaleString(),
                reviewPending: false,
            };
            this.persistPendingReview();
        },
        discardReviewResults() {
            this.resetReviewState();
            this.syncState = {
                ...this.syncState,
                reviewPending: false,
            };
            this.persistPendingReview();
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
                this.resetReviewState();
                const response = await syncProgressWithScreenshots(files, this.All_IDs);
                this.reviewState.images = this.buildReviewImages(files);
                this.reviewState.cards = (response.cards || []).map((card) => this.createReviewCard(card));
                this.reviewState.selectedCardId = this.reviewState.cards[0]?.id || null;
                this.syncState = {
                    loading: false,
                    processedScreenshots: response.processed_screenshots || files.length,
                    recognizedEntries: (response.cards || []).length,
                    matchedNames: (response.updates || []).map((item) => item.entryKey),
                    error: '',
                    updatedAt: new Date().toLocaleString(),
                    reviewPending: true,
                };
                this.persistPendingReview();
            } catch (error) {
                this.syncState = {
                    ...this.syncState,
                    loading: false,
                    error: error.message || this.$t('SyncFailed'),
                    reviewPending: false,
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
                reviewPending: false,
            };
            this.resetReviewState();
            this.persistProgress();
            this.persistPendingReview();
        },
    },
    async mounted() {
        this.restoreProgress();
        this.reviewPersistenceReady = true;
        await this.restorePendingReview();
    },
    async beforeUnmount() {
        await this.persistPendingReview();
        this.clearReviewImages();
    },
}
</script>

<style>
.cursor-crosshair {
    cursor: crosshair;
}
</style>


