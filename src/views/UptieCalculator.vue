<template>
    <div class="page-shell">
        <section class="page-grid">
            <div class="content-card overflow-hidden px-6 py-8 md:px-8">
                <div class="hero-grid items-start">
                    <div class="hero-card">
                        <p class="section-kicker">{{ $t(`UptieThreadPlanner`) }}</p>
                        <h1 class="section-title mt-3">{{ $t(`UptieCalculator`) }}</h1>
                        <p class="section-copy mt-4">{{ $t(`uptieCalculatorToolPage`) }}</p>
                    </div>

                    <div class="hero-card">
                        <p class="section-kicker">{{ $t(`UptieModes`) }}</p>
                        <div class="mt-4 grid gap-3 sm:grid-cols-2">
                            <button type="button" class="action-button action-button--accent" :disabled="!hasSavedProgress" :class="!hasSavedProgress ? 'cursor-not-allowed opacity-45' : ''" @click="calculate('uptie3')">{{ $t(`All Uptie 3`) }}</button>
                            <button type="button" class="action-button action-button--accent" :disabled="!hasSavedProgress" :class="!hasSavedProgress ? 'cursor-not-allowed opacity-45' : ''" @click="calculate('uptie4')">{{ $t(`All Uptie 4`) }}</button>
                            <button type="button" class="action-button" :disabled="!hasSavedProgress" :class="!hasSavedProgress ? 'cursor-not-allowed opacity-45' : ''" @click="calculate('uptie3only')">{{ $t(`All Uptie 3-2`) }}</button>
                            <button type="button" class="action-button" :disabled="!hasSavedProgress" :class="!hasSavedProgress ? 'cursor-not-allowed opacity-45' : ''" @click="calculate('uptie4only')">{{ $t(`All Uptie 4-2`) }}</button>
                        </div>

                        <div v-if="!hasSavedProgress" class="mt-4 rounded-[1.5rem] border border-gold/25 bg-black/25 p-4 text-sm text-stone-300">
                            <p class="font-accent uppercase tracking-[0.14em] text-gold">{{ $t(`UptieSetupRequiredTitle`) }}</p>
                            <p class="mt-2 leading-7 text-stone-300">{{ $t(`UptieSetupRequiredBody`) }}</p>
                            <button type="button" class="action-button mt-4 min-h-0 px-4 py-3" @click="goToStatusSetting()">{{ $t(`GoToStatusSetting`) }}</button>
                        </div>
                    </div>
                </div>

                <div class="mt-8 panel-divider"></div>

                <div class="mt-8 subtle-panel p-6">
                    <p class="section-kicker">{{ $t(`You need`) }}</p>
                    <div class="mt-4 muted-panel flex items-center gap-4 p-4">
                        <span class="deco-diamond shrink-0" aria-hidden="true"><img class="h-14 w-10" :alt="$t('Threads')" src="../../src/assets/icon_twine.webp"></span>
                        <div>
                            <p class="text-sm text-stone-400">{{ $t(`Threads`) }}</p>
                            <p class="deco-stat-value text-3xl">{{ CalResult.ThreadAmount }}</p>
                        </div>
                    </div>

                    <div class="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
                        <div v-for="shard in shardCards" :key="shard.key" class="muted-panel flex items-center gap-4 p-4">
                            <span class="deco-diamond shrink-0" aria-hidden="true"><img class="h-16 w-24" :alt="shard.key" :src="shard.image"></span>
                            <div>
                                <p class="text-sm text-stone-400">{{ $t(shard.label) }}</p>
                                <p class="font-accent text-2xl uppercase tracking-[0.14em] text-white">{{ CalResult[shard.key] }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>

<script>
import uptiethreadamount from '../components/uptiedata.js';
import { PROGRESS_STORAGE_KEY, PROGRESS_UPDATED_EVENT } from '../utils/progressSync';
import yiSangShardImage from '../assets/icon_piece-501YiSang.webp';
import faustShardImage from '../assets/icon_piece-502Faust.webp';
import donShardImage from '../assets/icon_piece-503DonQuixote.webp';
import ryoshuShardImage from '../assets/icon_piece-504Ryoshu.webp';
import meurShardImage from '../assets/icon_piece-505Meursault.webp';
import hongLuShardImage from '../assets/icon_piece-506HongLu.webp';
import heathShardImage from '../assets/icon_piece-507Heathcliff.webp';
import ishShardImage from '../assets/icon_piece-508Ishmael.webp';
import rodionShardImage from '../assets/icon_piece-509Rodion.webp';
import sinclairShardImage from '../assets/icon_piece-510EmilSinclair.webp';
import outisShardImage from '../assets/icon_piece-511Outis.webp';
import gregorShardImage from '../assets/icon_piece-512Gregor.webp';

export default {
    name: 'UptieCalculator',
    data() {
        return {
            CalResult: {
                ThreadAmount: 0,
                YiSangIDs: 0,
                FaustIDs: 0,
                DonIDs: 0,
                RyoshuIDs: 0,
                MeurIDs: 0,
                HongLuIDs: 0,
                HeathIDs: 0,
                RodionIDs: 0,
                IshIDs: 0,
                SinclairIDs: 0,
                OutisIDs: 0,
                GregorIDs: 0,
            },
            hasSavedProgress: false,
            shardCards: [
                { key: 'YiSangIDs', label: 'YiSang', image: yiSangShardImage },
                { key: 'FaustIDs', label: 'Faust', image: faustShardImage },
                { key: 'DonIDs', label: 'Don Quixote', image: donShardImage },
                { key: 'RyoshuIDs', label: 'Ryoshu', image: ryoshuShardImage },
                { key: 'MeurIDs', label: 'Meursault', image: meurShardImage },
                { key: 'HongLuIDs', label: 'Hong Lu', image: hongLuShardImage },
                { key: 'HeathIDs', label: 'Heathcliff', image: heathShardImage },
                { key: 'IshIDs', label: 'Ishmael', image: ishShardImage },
                { key: 'RodionIDs', label: 'Rodion', image: rodionShardImage },
                { key: 'SinclairIDs', label: 'Sinclair', image: sinclairShardImage },
                { key: 'OutisIDs', label: 'Outis', image: outisShardImage },
                { key: 'GregorIDs', label: 'Gregor', image: gregorShardImage },
            ],
            uptiethreadamount: uptiethreadamount.data().uptiethreadamount,
        }
    },
    methods: {
        syncSavedProgressState() {
            const stored = localStorage.getItem(PROGRESS_STORAGE_KEY);
            this.hasSavedProgress = Boolean(stored);
        },
        handleProgressUpdated() {
            this.syncSavedProgressState();
        },
        goToStatusSetting() {
            this.$router.push({ name: 'StatusSetting' });
        },
        calculateUptieCase(restore_data, mode) {
            this.CalResult.ThreadAmount = 0
            for (const [key1, value1] of Object.entries(restore_data)) {
                // console.log(key1);      //this.CalResult.YiSang,this.CalResult.Faust....
                var identityIDList = value1;//this.All_IDs.YiSangIDs,this.All_IDs.FaustIDs....
                var shardvalue = 0;
                var threadvalue = 0;
                var only_owned = (mode == "uptie3only") || (mode == "uptie4only") || (mode == "uptie5only");

                for (const [key2, value2] of Object.entries(identityIDList.IDs)) {
                    // console.log(key2, value2);
                    if (only_owned && value2.uptied == 0 && value2.rarity != "Rarity0") {
                        continue;
                    }
                    else {
                        if (value2.uptied < 1 && value2.rarity != "Rarity0") {
                            shardvalue += this.uptiethreadamount.sparkingshardamount[value2.rarity];
                        }
                        if (value2.uptied < 2) {
                            threadvalue += this.uptiethreadamount.IDamount[value2.rarity].from1to2.thread;
                        }
                        if (value2.uptied < 3) {
                            threadvalue += this.uptiethreadamount.IDamount[value2.rarity].from2to3.thread;
                        }
                        if (value2.uptied < 4 && !(mode == "uptie3only" || mode == "uptie3")) {
                            threadvalue += this.uptiethreadamount.IDamount[value2.rarity].from3to4.thread;
                            shardvalue += this.uptiethreadamount.IDamount[value2.rarity].from3to4.shard;
                        }
                    }

                }
                for (const [key3, value3] of Object.entries(identityIDList.EGOs)) {
                    //key3 = Chains of Others,Regret...
                    //value3 = { rarity: "Z", uptied: 0 },...
                    if (only_owned && value3.uptied == 0 && value3.rarity != "Z") {
                        continue;
                    }
                    else {
                        if (value3.uptied < 1 && value3.rarity != "Z") {
                            shardvalue += this.uptiethreadamount.sparkingshardamount.EGO;
                        }
                        if (value3.uptied < 2) {
                            threadvalue += this.uptiethreadamount.EGOamount[value3.rarity].from1to2.thread;
                        }
                        if (value3.uptied < 3) {
                            threadvalue += this.uptiethreadamount.EGOamount[value3.rarity].from2to3.thread;
                        }
                        if (value3.uptied < 4 && !(mode == "uptie3only" || mode == "uptie3")) {
                            threadvalue += this.uptiethreadamount.EGOamount[value3.rarity].from3to4.thread;
                            shardvalue += this.uptiethreadamount.EGOamount[value3.rarity].from3to4.shard;
                        }
                    }
                }
                this.CalResult.ThreadAmount += threadvalue;
                // console.log(key1, shardvalue);
                this.CalResult[key1] = shardvalue;
            }
        },
        calculate(mode) {
            // Store the mode in case will use it later
            localStorage.setItem('calmode', mode);
            this.syncSavedProgressState();
            let restore_data = null;
            try {
                restore_data = JSON.parse(localStorage.getItem(PROGRESS_STORAGE_KEY));
            } catch (e) {
                restore_data = null;
            }

            // If no account data, try to use local progress if available
            if (!restore_data) {
                // Try to use window.localProgress if present (legacy or fallback)
                if (window.localProgress) {
                    restore_data = window.localProgress;
                }
            }

            if (!restore_data) {
                alert(this.$t('dataNullAlert'));
                return;
            }

            this.calculateUptieCase(restore_data, mode);
        },
    },
    mounted() {
        this.syncSavedProgressState();
        window.addEventListener(PROGRESS_UPDATED_EVENT, this.handleProgressUpdated);
    },
    beforeUnmount() {
        window.removeEventListener(PROGRESS_UPDATED_EVENT, this.handleProgressUpdated);
    },
}
</script>

<style scoped>
.deco-diamond img {
    height: 4rem !important; /* 64px */
    width: 6rem !important;  /* 96px */
    max-width: none;
    max-height: none;
}
</style>
