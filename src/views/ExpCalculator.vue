<template>
    <div class="content">
        <div>
            <div class="box box1">
                <h1 class="subtitle">{{ $t(`ExpCalculator`) }}</h1>
                &nbsp;
                <h2 class="separator"></h2>
                &nbsp;
                <!-- <button @click="calEXPTesting()"></button> -->
                <div style="text-align: right;">
                    <div style="display:inline-flex;flex-flow:row wrap;justify-content: flex-end">
                        <div style="padding-right:10px">
                            <button class="button-6" role="button" @click="calculateExp('All35')">{{ $t(`All35`) }}
                            </button>
                            <button class="button-6" role="button" @click="calculateExp('All40')">{{ $t(`All40`) }}</button>
                            <!-- <button class="button-6" role="button" @click="updateuptiemode('uptie5')">{{ $t(`All Uptie 5`)}}</button> -->
                        </div>
                    </div>
                </div>
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
            expdata: expdata.data().expForEachLevel,
        }
    },
    methods: {
        calEXPTesting() {
            var sum = 0;
            for (let i = 0; i < this.expdata.length; i++) {
                sum += this.expdata[i];
            }
            console.log(sum); //should output 91700 when level cap is 40
        },

        calculateExp(mode) {
            //store the mode in case will use it later
            localStorage.setItem('expcalmode', mode);
            var restore_data = JSON.parse(localStorage.getItem('IDdata'));
            //set the value according to the mode
            restore_data ? this.calEXPTesting() : alert("Please import your data first!");
        },
    }
}
</script>

<style>
@import '../components/format.css';
</style>
