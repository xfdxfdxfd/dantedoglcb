<template>
    <div class="page-shell">
        <section class="page-grid">
            <div class="content-card overflow-hidden px-6 py-8 md:px-8">
                <div class="hero-grid items-start">
                    <div class="hero-card">
                        <p class="section-kicker">{{ $t(`UptieThreadPlanner`) }}</p>
                        <div class="deco-divider mt-4 lg:mx-0 lg:justify-start">{{ $t(`UptieGrandTotals`) }}</div>
                        <h1 class="section-title mt-3">{{ $t(`UptieCalculator`) }}</h1>
                        <p class="section-copy mt-4">{{ $t(`uptieCalculatorToolPage`) }}</p>
                    </div>

                    <div class="hero-card">
                        <p class="section-kicker">{{ $t(`UptieModes`) }}</p>
                        <div class="deco-divider mt-4">{{ $t(`UptieSelection`) }}</div>
                        <div class="mt-4 grid gap-3 sm:grid-cols-2">
                            <button type="button" class="action-button action-button--accent" @click="calculate('uptie3')">{{ $t(`All Uptie 3`) }}</button>
                            <button type="button" class="action-button action-button--accent" @click="calculate('uptie4')">{{ $t(`All Uptie 4`) }}</button>
                            <button type="button" class="action-button" @click="calculate('uptie3only')">{{ $t(`All Uptie 3-2`) }}</button>
                            <button type="button" class="action-button" @click="calculate('uptie4only')">{{ $t(`All Uptie 4-2`) }}</button>
                        </div>
                    </div>
                </div>

                <div class="mt-8 panel-divider"></div>

                <div class="mt-8 subtle-panel p-6">
                    <p class="section-kicker">{{ $t(`You need`) }}</p>
                    <div class="deco-divider mt-4 justify-start">{{ $t(`UptieThreadLedger`) }}</div>
                    <div class="mt-4 muted-panel flex items-center gap-4 p-4">
                        <span class="deco-diamond shrink-0" aria-hidden="true"><img class="h-6 w-6" :alt="$t('Threads')" src="../../src/assets/icon_twine.webp"></span>
                        <div>
                            <p class="text-sm text-stone-400">{{ $t(`Threads`) }}</p>
                            <p class="deco-stat-value text-3xl">{{ CalResult.ThreadAmount }}</p>
                        </div>
                    </div>

                    <div class="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
                        <div v-for="shard in shardCards" :key="shard.key" class="muted-panel flex items-center gap-4 p-4">
                            <span class="deco-diamond shrink-0" aria-hidden="true"><img class="h-6 w-6" :alt="shard.key" :src="shard.image"></span>
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
            shardCards: [
                { key: 'YiSangIDs', label: 'YiSang', image: require('../../src/assets/icon_piece-501YiSang.webp') },
                { key: 'FaustIDs', label: 'Faust', image: require('../../src/assets/icon_piece-502Faust.webp') },
                { key: 'DonIDs', label: 'Don Quixote', image: require('../../src/assets/icon_piece-503DonQuixote.webp') },
                { key: 'RyoshuIDs', label: 'Ryoshu', image: require('../../src/assets/icon_piece-504Ryoshu.webp') },
                { key: 'MeurIDs', label: 'Meursault', image: require('../../src/assets/icon_piece-505Meursault.webp') },
                { key: 'HongLuIDs', label: 'Hong Lu', image: require('../../src/assets/icon_piece-506HongLu.webp') },
                { key: 'HeathIDs', label: 'Heathcliff', image: require('../../src/assets/icon_piece-507Heathcliff.webp') },
                { key: 'IshIDs', label: 'Ishmael', image: require('../../src/assets/icon_piece-508Ishmael.webp') },
                { key: 'RodionIDs', label: 'Rodion', image: require('../../src/assets/icon_piece-509Rodion.webp') },
                { key: 'SinclairIDs', label: 'Sinclair', image: require('../../src/assets/icon_piece-510EmilSinclair.webp') },
                { key: 'OutisIDs', label: 'Outis', image: require('../../src/assets/icon_piece-511Outis.webp') },
                { key: 'GregorIDs', label: 'Gregor', image: require('../../src/assets/icon_piece-512Gregor.webp') },
            ],
            uptiethreadamount: uptiethreadamount.data().uptiethreadamount,
        }
    },
    methods: {
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
            //store the mode in case will use it later
            localStorage.setItem('calmode', mode);
            var restore_data = JSON.parse(localStorage.getItem('IDdata'));
            //set the value according to the mode
            restore_data ? this.calculateUptieCase(restore_data, mode) : alert(this.$t('dataNullAlert'));
        },
    },
}
</script>
