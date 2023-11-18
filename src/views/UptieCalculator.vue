<template>
    <div style="min-height: 100vh;" class="content">
        <div style="position: relative;">
            <div class="box box1">
                <h1 style="font-size: 40px;padding-top: 20px;color: #ffffff;">{{ $t(`UptieCalculator`) }}</h1>
                &nbsp;
                <h2 style="border-bottom: 3px solid rgb(172, 172, 172);"></h2>
                &nbsp;
                <h3 class="box1h3text" style="color:#c2bfbf;margin:10px">{{ $t(`UptieCalculatorSection2`) }}</h3>
                <div style="text-align: right;padding-right:10px">
                    <button class="button-6" role="button" style="background-color:rgb(255, 220, 161)"
                        @click="updateuptiemode('uptie3')">{{ $t(`All Uptie 3`)
                        }}</button>
                    <button class="button-6" role="button" style="background-color:rgb(255, 220, 161)"
                        @click="updateuptiemode('uptie4')">{{ $t(`All Uptie 4`)
                        }}</button>
                    <!-- <button class="button-6" role="button" @click="updateuptiemode('uptie5')">{{ $t(`All Uptie 5`)
                    }}</button> -->
                    <button class="button-6" role="button" @click="updateuptiemode('uptie3only')">{{ $t(`All Uptie 3-2`)
                    }}</button>
                    <button class="button-6" role="button" @click="updateuptiemode('uptie4only')">{{ $t(`All Uptie 4-2`)
                    }}</button>
                    <!-- <button class="button-6" role="button" @click="updateuptiemode('uptie5only')">{{ $t(`All Uptie 5-2`)}}</button> -->
                </div>
                <div style="text-align: right;padding-right:10px">
                    <button class="button-6" role="button" style="background-color:rgb(211, 55, 16);color:#fff">{{
                        $t(`Reset`)
                    }}</button>
                </div>
                <h2 style="border-bottom: 3px solid rgb(172, 172, 172);"></h2>
                &nbsp;
                <h3 class="box1h3text" style="text-align:left;">{{ $t(`You need`) }}:</h3>

                <!--result below-->
                <h2 class="box1h2text">
                    <div style="text-align: left;padding-left:100px">
                        <img class="shardimg" alt="ThreadAmount" src="../../src/assets/icon_twine.png">:{{
                            CalResult.ThreadAmount
                        }}&nbsp;
                    </div>
                    &nbsp;
                    <div>
                        <img class="shardimg" alt="YiSangShard" src="../../src/assets/icon_piece-501YiSang.png">:{{
                            CalResult.YiSang
                        }}&nbsp;
                        <img class="shardimg" alt="FaustShard" src="../../src/assets/icon_piece-502Faust.png">:{{
                            CalResult.Faust
                        }}&nbsp;
                        <img class="shardimg" alt="DonShard" src="../../src/assets/icon_piece-503DonQuixote.png">:{{
                            CalResult.Don
                        }}&nbsp;
                        <img class="shardimg" alt="RyoshuShard" src="../../src/assets/icon_piece-504Ryoshu.png">:{{
                            CalResult.Ryoshu
                        }}&nbsp;
                        <img class="shardimg" alt="MeurShard" src="../../src/assets/icon_piece-505Meursault.png">:{{
                            CalResult.Meur
                        }}&nbsp;
                        <img class="shardimg" alt="HongLuShard" src="../../src/assets/icon_piece-506HongLu.png">:{{
                            CalResult.HongLu
                        }}&nbsp;
                    </div>
                    <div>
                        <img class="shardimg" alt="HeathShard" src="../../src/assets/icon_piece-507Heathcliff.png">:{{
                            CalResult.Heath
                        }}&nbsp;
                        <img class="shardimg" alt="IshShard" src="../../src/assets/icon_piece-508Ishmael.png">:{{
                            CalResult.Ish
                        }}&nbsp;
                        <img class="shardimg" alt="RodionShard" src="../../src/assets/icon_piece-509Rodion.png">:{{
                            CalResult.Rodion
                        }}&nbsp;
                        <img class="shardimg" alt="SinclairShard" src="../../src/assets/icon_piece-510EmilSinclair.png">:{{
                            CalResult.Sinclair }}&nbsp;
                        <img class="shardimg" alt="OutisShard" src="../../src/assets/icon_piece-511Outis.png">:{{
                            CalResult.Outis
                        }}&nbsp;
                        <img class="shardimg" alt="GregorShard" src="../../src/assets/icon_piece-512Gregor.png">:{{
                            CalResult.Gregor
                        }}&nbsp;
                    </div>
                    &nbsp;
                </h2>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: 'UptieCalculator',
    data() {
        return {
            CalResult: {
                ThreadAmount: 0,
                YiSang: 0,
                Faust: 0,
                Don: 0,
                Ryoshu: 0,
                Meur: 0,
                HongLu: 0,
                Heath: 0,
                Rodion: 0,
                Ish: 0,
                Sinclair: 0,
                Outis: 0,
                Gregor: 0,
            },

            uptiethreadamount: {
                sparkingshardamount: {
                    "EGO": 400,
                    "000": 400,
                    "00": 150,
                },
                IDamount: {
                    "000": {
                        "1to2": { thread: 20, shard: 0 },
                        "2to3": { thread: 80, shard: 0 },
                        "3to4": { thread: 150, shard: 50 },
                    },
                    "00": {
                        "1to2": { thread: 10, shard: 0 },
                        "2to3": { thread: 40, shard: 0 },
                        "3to4": { thread: 100, shard: 30 },
                    },
                    "0": {
                        "1to2": { thread: 0, shard: 0 },
                        "2to3": { thread: 0, shard: 0 },
                        "3to4": { thread: 50, shard: 20 },
                    },
                },
                EGOamount: {
                    "Z": {
                        "1to2": { thread: 0, shard: 0 },
                        "2to3": { thread: 0, shard: 0 },
                        "3to4": { thread: 110, shard: 80 },
                    },
                    "ZnotOriginal": {
                        "1to2": { thread: 20, shard: 0 },
                        "2to3": { thread: 60, shard: 0 },
                        "3to4": { thread: 110, shard: 80 },
                    },
                    "T": {
                        "1to2": { thread: 25, shard: 0 },
                        "2to3": { thread: 70, shard: 0 },
                        "3to4": { thread: 130, shard: 90 },
                    },
                    "H": {
                        "1to2": { thread: 30, shard: 0 },
                        "2to3": { thread: 80, shard: 0 },
                        "3to4": { thread: 150, shard: 100 },
                    },
                }
            }
        }
    },
    computed: {
    },
    methods: {
        changewhichvalue(IDkey) {
            switch (IDkey) {
                case "YiSangIDs":
                    return this.CalResult.YiSang;
                case "FaustIDs":
                    return this.CalResult.Faust;
                case "DonIDs":
                    return this.CalResult.Don;
                case "RyoshuIDs":
                    return this.CalResult.Ryoshu;
                case "MeurIDs":
                    return this.CalResult.Meur;
                case "HongLuIDs":
                    return this.CalResult.HongLu;
                case "HeathIDs":
                    return this.CalResult.Heath;
                case "IshIDs":
                    return this.CalResult.Ish;
                case "RodionIDs":
                    return this.CalResult.Rodion;
                case "SinclairIDs":
                    return this.CalResult.Sinclair;
                case "OutisIDs":
                    return this.CalResult.Outis;
                case "GregorIDs":
                    return this.CalResult.Gregor;
                case "Threadamount":
                    return this.CalResult.ThreadAmount;
            }
        },

        calculate_case_ut3(restore_data) {
            for (const [key1, value1] of Object.entries(restore_data)) {
                var shardinput = this.changewhichvalue(key1);      //this.CalResult.YiSang,this.CalResult.Faust....
                var identityIDList = value1;                   //this.All_IDs.YiSangIDs,this.All_IDs.FaustIDs....
                for (const [key2, value2] of Object.entries(identityIDList.IDs)) {
                    //key2 = Molar Office Fixer Outis,LCB Sinner Meursault...
                    //value2 = { rarity: "000", uptied: 0 },...
                }
                for (const [key3, value3] of Object.entries(identityIDList.EGOs)) {
                    //key3 = Chains of Others,Regret...
                    //value3 = { rarity: "Z", uptied: 0 },...
                    //need to filter out the original EGOs for each Sinner
                }
            }
        },
        calculate_case_ut3only(restore_data) { },
        calculate_case_ut4(restore_data) { },
        calculate_case_ut4only(restore_data) { },
        calculate_case_ut5(restore_data) { },
        calculate_case_ut5only(restore_data) { },

        calculate(mode) {
            var restore_data = JSON.parse(localStorage.getItem('IDdata'));

            //set the value according to the mode
            if (restore_data) {
                switch (mode) {
                    case 'uptie3':
                        this.calculate_case_ut3(restore_data);
                        break;
                    case 'uptie3only':
                        this.calculate_case_ut3only(restore_data)
                        break;
                    case 'uptie4':
                        this.calculate_case_ut4(restore_data)
                        break;
                    case 'uptie4only':
                        this.calculate_case_ut4only(restore_data)
                        break;
                    case 'uptie5':
                        this.calculate_case_ut5(restore_data)
                        break;
                    case 'uptie5only':
                        this.calculate_case_ut5only(restore_data)
                        break;
                }
            }
        },

        updateuptiemode(mode) {
            localStorage.setItem('calmode', mode);
        },
    },
    mounted() {
        // //call restoreprogress funct when DOMContentLoaded
        // document.addEventListener('DOMContentLoaded', this.calculateresult);
        // //reload the page for addeventlistener rlly show result
        // if (localStorage.getItem('reloaded')) { //just reloaded
        //     localStorage.removeItem('reloaded');
        // } else {
        //     // Set a flag so that we know not to reload the page twice.
        //     localStorage.setItem('reloaded', '1');
        //     location.reload();
        // }
    },
    watch: {
    }
}
</script>

<style>
.shardimg {
    width: 50px
}
</style>