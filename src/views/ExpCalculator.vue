<template>
    <div class="page-shell">
        <section class="mx-auto max-w-7xl px-4 py-8 md:px-6 lg:px-8">
            <div class="content-card overflow-hidden px-6 py-8 md:px-8">
                <div class="flex flex-col gap-8 xl:flex-row xl:items-end xl:justify-between">
                    <div class="max-w-3xl">
                        <p class="field-label text-gold">EXP Planner</p>
                        <h1 class="section-title mt-3">{{ $t(`ExpCalculator`) }}</h1>
                        <p class="section-copy mt-4">{{ $t(`ExpCalculatorToolPage`) }}</p>
                    </div>

                    <div class="grid gap-3 sm:grid-cols-3">
                        <button type="button" class="action-button" @click="calculateExp('All35'); calculateExpCase_Ticket();">{{ $t(`All35`) }}</button>
                        <button type="button" class="action-button action-button--accent" @click="calculateExp('All40'); calculateExpCase_Ticket();">{{ $t(`All40`) }}</button>
                        <button type="button" class="action-button action-button--accent" @click="calculateExp('All45'); calculateExpCase_Ticket();">{{ $t(`All45`) }}</button>
                    </div>
                </div>

                <div class="mt-8 grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
                    <div class="rounded-[2rem] border border-white/10 bg-black/20 p-6">
                        <p class="field-label">{{ $t(`You need`) }}</p>
                        <p class="mt-4 text-4xl font-bold text-white">{{ calExpResult }}</p>
                        <p class="mt-2 text-sm text-stone-400">{{ $t(`Exp`) }}</p>
                    </div>

                    <div class="rounded-[2rem] border border-white/10 bg-black/20 p-6">
                        <p class="field-label">{{ $t(`Which is about`) }}</p>
                        <div class="mt-5 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
                            <div v-for="ticket in ticketCards" :key="ticket.label" class="rounded-2xl border border-white/10 bg-white/5 p-4">
                                <img class="h-12 w-auto" :alt="ticket.label" :src="ticket.image">
                                <p class="mt-3 text-sm text-stone-400">{{ ticket.label }}</p>
                                <p class="mt-1 text-2xl font-bold text-white">{{ ticket.value }}</p>
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
        }
    },
    computed: {
        ticketCards() {
            return [
                { label: 'Ticket IV', value: this.TicketIV, image: require('../../src/assets/Identity_Training_Ticket_IV.webp') },
                { label: 'Ticket III', value: this.TicketIII, image: require('../../src/assets/Identity_Training_Ticket_III.webp') },
                { label: 'Ticket II', value: this.TicketII, image: require('../../src/assets/Identity_Training_Ticket_II.webp') },
                { label: 'Ticket I', value: this.TicketI, image: require('../../src/assets/Identity_Training_Ticket_I.webp') },
            ];
        },
    },
    methods: {
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
            var restore_data = JSON.parse(localStorage.getItem('IDdata'));
            //set the value according to the mode
            restore_data ? this.calculateExpCase(restore_data, mode) : alert(this.$t('dataNullAlert'));
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
    }
}
</script>
