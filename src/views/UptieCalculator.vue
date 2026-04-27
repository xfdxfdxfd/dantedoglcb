<template>
    <div class="page-shell">
        <section class="mx-auto max-w-7xl px-4 py-8 md:px-6 lg:px-8">
            <div class="content-card overflow-hidden px-6 py-8 md:px-8">
                <div class="flex flex-col gap-8 xl:flex-row xl:items-end xl:justify-between">
                    <div class="max-w-3xl">
                        <p class="field-label text-gold">Thread Planner</p>
                        <h1 class="section-title mt-3">{{ $t(`UptieCalculator`) }}</h1>
                        <p class="section-copy mt-4">{{ $t(`uptieCalculatorToolPage`) }}</p>
                    </div>

                    <div class="grid gap-3 sm:grid-cols-2">
                        <button type="button" class="action-button action-button--accent" @click="calculate('uptie3')">{{ $t(`All Uptie 3`) }}</button>
                        <button type="button" class="action-button action-button--accent" @click="calculate('uptie4')">{{ $t(`All Uptie 4`) }}</button>
                        <button type="button" class="action-button" @click="calculate('uptie3only')">{{ $t(`All Uptie 3-2`) }}</button>
                        <button type="button" class="action-button" @click="calculate('uptie4only')">{{ $t(`All Uptie 4-2`) }}</button>
                    </div>
                </div>

                <div class="mt-8 panel-divider"></div>

                <div class="mt-8 rounded-[2rem] border border-white/10 bg-black/20 p-6">
                    <p class="field-label">{{ $t(`You need`) }}</p>
                    <div class="mt-4 flex items-center gap-4 rounded-2xl border border-white/10 bg-white/5 p-4">
                        <img class="h-10 w-10" alt="ThreadAmount" src="../../src/assets/icon_twine.webp">
                        <div>
                            <p class="text-sm text-stone-400">Threads</p>
                            <p class="text-3xl font-bold text-white">{{ CalResult.ThreadAmount }}</p>
                        </div>
                    </div>

                    <div class="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
                        <div v-for="shard in shardCards" :key="shard.key" class="flex items-center gap-4 rounded-2xl border border-white/10 bg-white/5 p-4">
                            <img class="h-10 w-10" :alt="shard.key" :src="shard.image">
                            <div>
                                <p class="text-sm text-stone-400">{{ $t(shard.label) }}</p>
                                <p class="text-2xl font-bold text-white">{{ CalResult[shard.key] }}</p>
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
