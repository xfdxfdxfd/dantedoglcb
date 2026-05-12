<template>
    <div class="page-shell">
        <section class="page-grid">
            <div class="content-card overflow-hidden px-6 py-8 md:px-8">
                <div class="hero-grid items-start">
                    <div class="hero-card">
                        <p class="section-kicker">{{ $t(`ExpPlanner`) }}</p>
                        <div class="deco-divider mt-4 lg:mx-0 lg:justify-start">{{ $t(`ExpTrainingBureau`) }}</div>
                        <h1 class="section-title mt-3">{{ $t(`ExpCalculator`) }}</h1>
                        <p class="section-copy mt-4">{{ $t(`ExpCalculatorToolPage`) }}</p>
                    </div>

                    <div class="hero-card">
                        <p class="section-kicker">{{ $t(`ExpTargetLevel`) }}</p>
                        <div class="deco-divider mt-4">{{ $t(`ExpCeiling`) }}</div>
                        <div class="mt-4 grid gap-3 sm:grid-cols-3">
                            <button type="button" class="action-button" :disabled="!hasSavedProgress" :class="!hasSavedProgress ? 'cursor-not-allowed opacity-45' : ''" @click="calculateExp('All35'); calculateExpCase_Ticket();">{{ $t(`All35`) }}</button>
                            <button type="button" class="action-button action-button--accent" :disabled="!hasSavedProgress" :class="!hasSavedProgress ? 'cursor-not-allowed opacity-45' : ''" @click="calculateExp('All40'); calculateExpCase_Ticket();">{{ $t(`All40`) }}</button>
                            <button type="button" class="action-button action-button--accent" :disabled="!hasSavedProgress" :class="!hasSavedProgress ? 'cursor-not-allowed opacity-45' : ''" @click="calculateExp('All45'); calculateExpCase_Ticket();">{{ $t(`All45`) }}</button>
                        </div>

                        <div v-if="!hasSavedProgress" class="mt-4 rounded-[1.5rem] border border-gold/25 bg-black/25 p-4 text-sm text-stone-300">
                            <p class="font-accent uppercase tracking-[0.14em] text-gold">{{ $t(`ExpSetupRequiredTitle`) }}</p>
                            <p class="mt-2 leading-7 text-stone-300">{{ $t(`ExpSetupRequiredBody`) }}</p>
                            <button type="button" class="action-button mt-4 min-h-0 px-4 py-3" @click="goToStatusSetting()">{{ $t(`GoToStatusSetting`) }}</button>
                        </div>
                    </div>
                </div>

                <div class="mt-8 grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
                    <div class="subtle-panel p-6">
                        <p class="section-kicker">{{ $t(`You need`) }}</p>
                        <div class="deco-divider mt-4 justify-start">{{ $t(`ExpReserve`) }}</div>
                        <p class="deco-stat-value mt-4">{{ calExpResult }}</p>
                        <p class="mt-2 text-sm text-stone-400">{{ $t(`Exp`) }}</p>
                    </div>

                    <div class="subtle-panel p-6">
                        <p class="section-kicker">{{ $t(`Which is about`) }}</p>
                        <div class="deco-divider mt-4 justify-start">{{ $t(`ExpTicketStack`) }}</div>
                        <div class="mt-5 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
                            <div v-for="ticket in ticketCards" :key="ticket.key" class="muted-panel p-4">
                                <div class="deco-image-frame inline-block">
                                    <img class="block h-12 max-w-full object-contain grayscale" :alt="ticket.label" :src="ticket.image">
                                </div>
                                <p class="mt-3 text-sm text-stone-400">{{ ticket.label }}</p>
                                <p class="mt-1 font-accent text-2xl uppercase tracking-[0.14em] text-white">{{ ticket.value }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>

<script>
import expdata from '../components/expdata.js'
import { PROGRESS_STORAGE_KEY, PROGRESS_UPDATED_EVENT } from '../utils/progressSync';
import ticketIImage from '../assets/Identity_Training_Ticket_I.webp';
import ticketIIImage from '../assets/Identity_Training_Ticket_II.webp';
import ticketIIIImage from '../assets/Identity_Training_Ticket_III.webp';
import ticketIVImage from '../assets/Identity_Training_Ticket_IV.webp';

export default {
    name: 'ExpCalculator',
    data() {
        return {
            expdata: expdata.data(),
            calExpResult: 0,
            TicketIV: 0,
            TicketIII: 0,
            TicketII: 0,
            TicketI: 0,
            hasSavedProgress: false,
        }
    },
    computed: {
        ticketCards() {
            return [
                { key: 'TicketIV', label: this.$t('TicketIV'), value: this.TicketIV, image: ticketIVImage },
                { key: 'TicketIII', label: this.$t('TicketIII'), value: this.TicketIII, image: ticketIIIImage },
                { key: 'TicketII', label: this.$t('TicketII'), value: this.TicketII, image: ticketIIImage },
                { key: 'TicketI', label: this.$t('TicketI'), value: this.TicketI, image: ticketIImage },
            ];
        },
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
        calEXPTesting() {
            //accum exp up to 40: 91700 accum exp up to 35: 61123
            // var listOfSum = [];
            // var listOfSum2 = [];
            // for (let i = 0; i < this.expdata.expAccumulatedUpTo40.length; i++) {
            //     listOfSum.push(this.expdata.expAccumulatedUpTo40[i]);
            // }
            // for (let i = 0; i < this.expdata.expAccumulatedUpTo35.length; i++) {
            //     listOfSum2.push(this.expdata.expAccumulatedUpTo35[i]);
            // }
            let sum = 0;
            for (let i = 0; i < this.expdata.expForEachLevel.length; i++) {
                sum += this.expdata.expForEachLevel[i];
            }
            console.log(sum);
            let listOfSum = [sum];
            for (let j = 0; j < this.expdata.expForEachLevel.length; j++) {
                sum = sum - this.expdata.expForEachLevel[j]
                listOfSum.push(sum);
            }
            console.log(listOfSum);

        },

        getRemainingExp(expTable, level) {
            const clampedIndex = Math.min(Math.max(parseInt(level, 10) || 1, 1), expTable.length) - 1;
            return parseInt(expTable[clampedIndex] || 0);
        },
        calculateExpCase(restore_data, mode) {
            var totalExpSum = 0;
            for (const [key1, value1] of Object.entries(restore_data)) {
                var expSum = 0;
                if (mode == 'All35') {
                    for (const [key2, value2] of Object.entries(value1.IDs)) { expSum += this.getRemainingExp(this.expdata.expAccumulatedUpTo35, value2.level); }
                    totalExpSum += expSum;

                } else if (mode == 'All40') {
                    for (const [key2, value2] of Object.entries(value1.IDs)) { expSum += this.getRemainingExp(this.expdata.expAccumulatedUpTo40, value2.level); }
                    totalExpSum += expSum;

                } else if (mode == 'All45') {
                    for (const [key2, value2] of Object.entries(value1.IDs)) { expSum += this.getRemainingExp(this.expdata.expAccumulatedUpTo45, value2.level); }
                    totalExpSum += expSum;
                }
            }
            this.calExpResult = totalExpSum;
            // console.log(this.calExpResult);
        },

        calculateExp(mode) {
            //store the mode in case will use it later
            localStorage.setItem('expcalmode', mode);
            this.syncSavedProgressState();
            var restore_data = JSON.parse(localStorage.getItem(PROGRESS_STORAGE_KEY));
            //set the value according to the mode
            if (!restore_data) {
                alert(this.$t('dataNullAlert'));
                return;
            }

            this.calculateExpCase(restore_data, mode);
        },
        calculateExpCase_Ticket() {
            this.TicketIV = parseInt(parseInt(this.calExpResult) / 3000);
            this.TicketIII = parseInt((parseInt(this.calExpResult) % 3000) / 1000);
            this.TicketII = parseInt((parseInt(this.calExpResult) % 1000) / 200);
            var IDI = parseInt((parseInt(this.calExpResult) % 200) / 50);
            parseInt((parseInt(this.calExpResult) % 50)) > 0 ? IDI += 1 : IDI;
            this.TicketI = IDI;
            // console.log(this.TicketIV, this.TicketIII, this.TicketII, this.TicketI);

        }
    },
    mounted() {
        this.syncSavedProgressState();
        window.addEventListener(PROGRESS_UPDATED_EVENT, this.handleProgressUpdated);
    },
    beforeUnmount() {
        window.removeEventListener(PROGRESS_UPDATED_EVENT, this.handleProgressUpdated);
    }
}
</script>
