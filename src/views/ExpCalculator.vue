<template>
    <div class="content">
        <div>
            <div class="box box1">
                <h1 class="subtitle">{{ $t(`ExpCalculator`) }}</h1>
                &nbsp;
                <h2 class="separator"></h2>
                &nbsp;
                <h3 class="box1h3text" style="color:#c2bfbf;margin:10px">{{ $t(`ExpCalculatorToolPage`) }}</h3>
                <div style="text-align: right;">
                    <div style="display:inline-flex;flex-flow:row wrap;justify-content: flex-end">
                        <div style="padding-right:10px">
                            <button class="button-6" role="button"
                                @click="calculateExp('All35'), calculateExpCase_Ticket()">{{ $t(`All35`) }}</button>
                            <button class="button-6" role="button"
                                @click="calculateExp('All40'), calculateExpCase_Ticket()">{{ $t(`All40`) }}</button>
                            <!-- <button @click="calEXPTesting()"></button> -->
                        </div>
                    </div>
                </div>
                <h2 class="separator"></h2>
                &nbsp;
                <h3 class="box1h3text" style="text-align:left;">{{ $t(`You need`) }}: {{ calExpResult }} {{ $t(`Exp`) }}
                </h3>
                &nbsp;
                <h3 class="box1h3text" style="text-align:left;">{{ $t(`Which is about`) }}:</h3>
                <h2 class="box1h2text">
                    <div class="resultimg">
                        <div>
                            <img class="ticketimg" alt="IVAmount"
                                src="../../src/assets/Identity_Training_Ticket_IV.webp">:{{ TicketIV }}
                        </div>
                        &nbsp;
                        <div>
                            <img class="ticketimg" alt="IIIAmount"
                                src="../../src/assets/Identity_Training_Ticket_III.webp">:{{ TicketIII }}
                        </div>
                        &nbsp;
                        <div>
                            <img class="ticketimg" alt="IIAmount"
                                src="../../src/assets/Identity_Training_Ticket_II.webp">:{{ TicketII }}
                        </div>
                        &nbsp;
                        <div>
                            <img class="ticketimg" alt="IAmount" src="../../src/assets/Identity_Training_Ticket_I.webp">:{{
                                TicketI }}
                        </div>
                        &nbsp;
                    </div>
                </h2>
            </div>
        </div>
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
    methods: {
        calEXPTesting() {
            //accum exp up to 40: 91700 accum exp up to 35: 61123
            var listOfSum = [];
            var listOfSum2 = [];
            for (let i = 0; i < this.expdata.expAccumulatedUpTo40.length; i++) {
                listOfSum.push(this.expdata.expAccumulatedUpTo40[i]);
            }
            for (let i = 0; i < this.expdata.expAccumulatedUpTo35.length; i++) {
                listOfSum2.push(this.expdata.expAccumulatedUpTo35[i]);
            }
            // console.log(listOfSum, listOfSum2);
        },

        calculateExpCase(restore_data, mode) {
            var totalExpSum = 0;
            for (const [key1, value1] of Object.entries(restore_data)) {
                var expSum = 0;
                if (mode == 'All35') {
                    for (const [key2, value2] of Object.entries(value1.IDs)) { expSum += parseInt(this.expdata.expAccumulatedUpTo35[parseInt(value2.level) - 1]); }
                    totalExpSum += expSum;

                } else if (mode == 'All40') {
                    for (const [key2, value2] of Object.entries(value1.IDs)) { expSum += parseInt(this.expdata.expAccumulatedUpTo40[parseInt(value2.level) - 1]); }
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
            console.log(this.TicketIV, this.TicketIII, this.TicketII, this.TicketI);

        }
    }
}
</script>

<style>@import '../components/format.css';</style>
