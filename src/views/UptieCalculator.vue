<template>
    <div class="content">
        <div>
            <div class="box box1">
                <h1 class="subtitle">{{ $t(`UptieCalculator`) }}</h1>
                &nbsp;
                <h2 class="separator"></h2>
                &nbsp;
                <h3 class="box1h3text" style="color:#c2bfbf;margin:10px">{{ $t(`uptieCalculatorToolPage`) }}</h3>
                <div style="text-align: right;">
                    <div style="display:inline-flex;flex-flow:row wrap;justify-content: flex-end">
                        <div style="padding-right:10px">
                            <button class="button-6" role="button" style="background-color:rgb(255, 220, 161)"
                                @click="calculate('uptie3')">{{ $t(`All Uptie 3`)
                                }}</button>
                            <button class="button-6" role="button" style="background-color:rgb(255, 220, 161)"
                                @click="calculate('uptie4')">{{ $t(`All Uptie 4`)
                                }}</button>
                            <!-- <button class="button-6" role="button" @click="calculate('uptie5')">{{ $t(`All Uptie 5`)}}</button> -->
                        </div>
                        <div style="padding-right:10px">
                            <button class="button-6" role="button" @click="calculate('uptie3only')">{{
                                $t(`All Uptie 3-2`)
                            }}</button>
                            <button class="button-6" role="button" @click="calculate('uptie4only')">{{ $t(`All Uptie 4-2`)
                            }}</button>
                            <!-- <button class="button-6" role="button" @click="calculate('uptie5only')">{{ $t(`All Uptie 5-2`)}}</button> -->
                        </div>
                    </div>
                </div>
                <h2 class="separator"></h2>
                &nbsp;
                <h3 class="box1h3text" style="text-align:left;">{{ $t(`You need`) }}:</h3>

                <!--result below-->
                <h2 class="box1h2text">
                    <div style="text-align: left;padding-left:5vw">
                        <img class="shardimg" alt="ThreadAmount" src="../../src/assets/icon_twine.webp">:{{
                            CalResult.ThreadAmount
                        }}&nbsp;
                    </div>
                    &nbsp;
                    <div class="resultimg">
                        <div>
                            <img class="shardimg" alt="YiSangShard" src="../../src/assets/icon_piece-501YiSang.webp">:{{
                                CalResult.YiSangIDs
                            }}
                        </div>
                        <div>
                            <img class="shardimg" alt="FaustShard" src="../../src/assets/icon_piece-502Faust.webp">:{{
                                CalResult.FaustIDs
                            }}
                        </div>
                        <div>
                            <img class="shardimg" alt="DonShard" src="../../src/assets/icon_piece-503DonQuixote.webp">:{{
                                CalResult.DonIDs
                            }}
                        </div>
                        <div>
                            <img class="shardimg" alt="RyoshuShard" src="../../src/assets/icon_piece-504Ryoshu.webp">:{{
                                CalResult.RyoshuIDs
                            }}
                        </div>
                        <div>
                            <img class="shardimg" alt="MeurShard" src="../../src/assets/icon_piece-505Meursault.webp">:{{
                                CalResult.MeurIDs
                            }}
                        </div>
                        <div>
                            <img class="shardimg" alt="HongLuShard" src="../../src/assets/icon_piece-506HongLu.webp">:{{
                                CalResult.HongLuIDs
                            }}
                        </div>
                        <div>
                            <img class="shardimg" alt="HeathShard" src="../../src/assets/icon_piece-507Heathcliff.webp">:{{
                                CalResult.HeathIDs
                            }}
                        </div>
                        <div>
                            <img class="shardimg" alt="IshShard" src="../../src/assets/icon_piece-508Ishmael.webp">:{{
                                CalResult.IshIDs
                            }}
                        </div>
                        <div>
                            <img class="shardimg" alt="RodionShard" src="../../src/assets/icon_piece-509Rodion.webp">:{{
                                CalResult.RodionIDs
                            }}
                        </div>
                        <div>
                            <img class="shardimg" alt="SinclairShard"
                                src="../../src/assets/icon_piece-510EmilSinclair.webp">:{{ CalResult.SinclairIDs }}
                        </div>
                        <div>
                            <img class="shardimg" alt="OutisShard" src="../../src/assets/icon_piece-511Outis.webp">:{{
                                CalResult.OutisIDs
                            }}
                        </div>
                        <div>
                            <img class="shardimg" alt="GregorShard" src="../../src/assets/icon_piece-512Gregor.webp">:{{
                                CalResult.GregorIDs
                            }}
                        </div>
                    </div>
                </h2>
            </div>
        </div>
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

            uptiethreadamount: uptiethreadamount.data().uptiethreadamount,
        }
    },
    computed: {
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
    mounted() {
    },
    watch: {
    }
}
</script>

<style>
@import '../components/format.css';
</style>