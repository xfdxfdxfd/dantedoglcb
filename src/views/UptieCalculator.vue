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
                        @click="updateuptiemode('uptie3'), calculate('uptie3')">{{ $t(`All Uptie 3`)
                        }}</button>
                    <button class="button-6" role="button" style="background-color:rgb(255, 220, 161)"
                        @click="updateuptiemode('uptie4'), calculate('uptie4')">{{ $t(`All Uptie 4`)
                        }}</button>
                    <!-- <button class="button-6" role="button" @click="updateuptiemode('uptie5')">{{ $t(`All Uptie 5`)
                    }}</button> -->
                    <button class="button-6" role="button"
                        @click="updateuptiemode('uptie3only'), calculate('uptie3only')">{{
                            $t(`All Uptie 3-2`)
                        }}</button>
                    <button class="button-6" role="button"
                        @click="updateuptiemode('uptie4only'), calculate('uptie4only')">{{ $t(`All Uptie 4-2`)
                        }}</button>
                    <!-- <button class="button-6" role="button" @click="updateuptiemode('uptie5only')">{{ $t(`All Uptie 5-2`)}}</button> -->
                </div>
                <!-- <div style="text-align: right;padding-right:10px">
                    <button class="button-6" role="button" style="background-color:rgb(211, 55, 16);color:#fff">{{
                        $t(`Reset`)
                    }}</button>
                </div> -->
                <h2 style="border-bottom: 3px solid rgb(172, 172, 172);"></h2>
                &nbsp;
                <h3 class="box1h3text" style="text-align:left;">{{ $t(`You need`) }}:</h3>

                <!--result below-->
                <h2 class="box1h2text">
                    <div style="text-align: left;padding-left:5vw">
                        <img class="shardimg" alt="ThreadAmount" src="../../src/assets/icon_twine.png">:{{
                            CalResult.ThreadAmount
                        }}&nbsp;
                    </div>
                    &nbsp;
                    <div>
                        <img class="shardimg" alt="YiSangShard" src="../../src/assets/icon_piece-501YiSang.png">:{{
                            CalResult.YiSangIDs
                        }}&nbsp;
                        <img class="shardimg" alt="FaustShard" src="../../src/assets/icon_piece-502Faust.png">:{{
                            CalResult.FaustIDs
                        }}&nbsp;
                        <img class="shardimg" alt="DonShard" src="../../src/assets/icon_piece-503DonQuixote.png">:{{
                            CalResult.DonIDs
                        }}&nbsp;
                        <img class="shardimg" alt="RyoshuShard" src="../../src/assets/icon_piece-504Ryoshu.png">:{{
                            CalResult.RyoshuIDs
                        }}&nbsp;
                        <img class="shardimg" alt="MeurShard" src="../../src/assets/icon_piece-505Meursault.png">:{{
                            CalResult.MeurIDs
                        }}&nbsp;
                        <img class="shardimg" alt="HongLuShard" src="../../src/assets/icon_piece-506HongLu.png">:{{
                            CalResult.HongLuIDs
                        }}&nbsp;
                    </div>
                    <div>
                        <img class="shardimg" alt="HeathShard" src="../../src/assets/icon_piece-507Heathcliff.png">:{{
                            CalResult.HeathIDs
                        }}&nbsp;
                        <img class="shardimg" alt="IshShard" src="../../src/assets/icon_piece-508Ishmael.png">:{{
                            CalResult.IshIDs
                        }}&nbsp;
                        <img class="shardimg" alt="RodionShard" src="../../src/assets/icon_piece-509Rodion.png">:{{
                            CalResult.RodionIDs
                        }}&nbsp;
                        <img class="shardimg" alt="SinclairShard" src="../../src/assets/icon_piece-510EmilSinclair.png">:{{
                            CalResult.SinclairIDs }}&nbsp;
                        <img class="shardimg" alt="OutisShard" src="../../src/assets/icon_piece-511Outis.png">:{{
                            CalResult.OutisIDs
                        }}&nbsp;
                        <img class="shardimg" alt="GregorShard" src="../../src/assets/icon_piece-512Gregor.png">:{{
                            CalResult.GregorIDs
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

            uptiethreadamount: {
                sparkingshardamount: {
                    "EGO": 400,
                    "Rarity000": 400,
                    "Rarity00": 150,
                    "Rarity0": 0,
                },
                IDamount: {
                    "Rarity000": {
                        "from1to2": { thread: 20, shard: 0 },
                        "from2to3": { thread: 80, shard: 0 },
                        "from3to4": { thread: 150, shard: 50 },
                    },
                    "Rarity00": {
                        "from1to2": { thread: 10, shard: 0 },
                        "from2to3": { thread: 40, shard: 0 },
                        "from3to4": { thread: 100, shard: 30 },
                    },
                    "Rarity0": {
                        "from1to2": { thread: 0, shard: 0 },
                        "from2to3": { thread: 0, shard: 0 },
                        "from3to4": { thread: 50, shard: 20 },
                    },
                },
                EGOamount: {
                    "Z": {
                        "from1to2": { thread: 0, shard: 0 },
                        "from2to3": { thread: 0, shard: 0 },
                        "from3to4": { thread: 110, shard: 80 },
                    },
                    "ZnotOriginal": {
                        "from1to2": { thread: 20, shard: 0 },
                        "from2to3": { thread: 60, shard: 0 },
                        "from3to4": { thread: 110, shard: 80 },
                    },
                    "T": {
                        "from1to2": { thread: 25, shard: 0 },
                        "from2to3": { thread: 70, shard: 0 },
                        "from3to4": { thread: 130, shard: 90 },
                    },
                    "H": {
                        "from1to2": { thread: 30, shard: 0 },
                        "from2to3": { thread: 80, shard: 0 },
                        "from3to4": { thread: 150, shard: 100 },
                    },
                    "W": {
                        "from1to2": { thread: 35, shard: 0 },
                        "from2to3": { thread: 90, shard: 0 },
                        "from3to4": { thread: 170, shard: 150 },
                    }
                }
            },

            ZEGOnotOriginal: {
                Soda: "Soda",
                Legerdemain: "Legerdemain",
            }
        }
    },
    computed: {
    },
    methods: {

        calculate_case_ut3(restore_data) {
            this.CalResult.ThreadAmount = 0
            for (const [key1, value1] of Object.entries(restore_data)) {
                // console.log(key1);      //this.CalResult.YiSang,this.CalResult.Faust....
                var identityIDList = value1;//this.All_IDs.YiSangIDs,this.All_IDs.FaustIDs....
                var shardvalue = 0;
                var threadvalue = 0;
                for (const [key2, value2] of Object.entries(identityIDList.IDs)) {
                    //key2 = Molar Office Fixer Outis,LCB Sinner Meursault...
                    //value2 = { rarity: "000", uptied: 0 },...
                    switch (value2.rarity) {
                        case "000":
                            if (value2.uptied == "2") { //ut2 or below
                                threadvalue += this.uptiethreadamount.IDamount.Rarity000.from2to3.thread;
                            }
                            if (value2.uptied == "1") { //ut1 or don't hv
                                threadvalue += this.uptiethreadamount.IDamount.Rarity000.from2to3.thread;
                                threadvalue += this.uptiethreadamount.IDamount.Rarity000.from1to2.thread;
                            }
                            if (value2.uptied == "0") { //don't hv
                                threadvalue += this.uptiethreadamount.IDamount.Rarity000.from2to3.thread;
                                threadvalue += this.uptiethreadamount.IDamount.Rarity000.from1to2.thread;
                                shardvalue += this.uptiethreadamount.sparkingshardamount.Rarity000;
                            }
                            break;
                        case "00":
                            if (value2.uptied == "2") { //ut2 or below
                                threadvalue += this.uptiethreadamount.IDamount.Rarity00.from2to3.thread;
                            }
                            if (value2.uptied == "1") { //ut1 or don't hv
                                threadvalue += this.uptiethreadamount.IDamount.Rarity00.from2to3.thread;
                                threadvalue += this.uptiethreadamount.IDamount.Rarity00.from1to2.thread;
                            }
                            if (value2.uptied == "0") { //don't hv
                                threadvalue += this.uptiethreadamount.IDamount.Rarity00.from2to3.thread;
                                threadvalue += this.uptiethreadamount.IDamount.Rarity00.from1to2.thread;
                                shardvalue += this.uptiethreadamount.sparkingshardamount.Rarity00;
                            }
                            break;
                        case "0": //do nothing as lcb sinner only do ut4
                            break;
                    }
                }
                for (const [key3, value3] of Object.entries(identityIDList.EGOs)) {
                    //key3 = Chains of Others,Regret...
                    //value3 = { rarity: "Z", uptied: 0 },...
                    //need to filter out the original EGOs for each Sinner
                    switch (value3.rarity) {
                        case "W":
                            if (value3.uptied == "2") { //ut2 or below
                                //console.log("value3.uptied = 2")
                                threadvalue += this.uptiethreadamount.EGOamount.W.from2to3.thread;
                            }
                            if (value3.uptied == "1") { //ut1 or don't hv
                                //console.log("value3.uptied = 1")
                                threadvalue += this.uptiethreadamount.EGOamount.W.from2to3.thread;
                                threadvalue += this.uptiethreadamount.EGOamount.W.from1to2.thread;
                            }
                            if (value3.uptied == "0") { //don't hv
                                //console.log("value3.uptied = 0")
                                threadvalue += this.uptiethreadamount.EGOamount.W.from2to3.thread;
                                threadvalue += this.uptiethreadamount.EGOamount.W.from1to2.thread;
                                shardvalue += this.uptiethreadamount.sparkingshardamount.EGO;
                            }
                            break;
                        case "T":
                            if (value3.uptied == "2") { //ut2 or below
                                //console.log("value3.uptied = 2")
                                threadvalue += this.uptiethreadamount.EGOamount.T.from2to3.thread;
                            }
                            if (value3.uptied == "1") { //ut1 or don't hv
                                //console.log("value3.uptied = 1")
                                threadvalue += this.uptiethreadamount.EGOamount.T.from2to3.thread;
                                threadvalue += this.uptiethreadamount.EGOamount.T.from1to2.thread;
                            }
                            if (value3.uptied == "0") { //don't hv
                                //console.log("value3.uptied = 0")
                                threadvalue += this.uptiethreadamount.EGOamount.T.from2to3.thread;
                                threadvalue += this.uptiethreadamount.EGOamount.T.from1to2.thread;
                                shardvalue += this.uptiethreadamount.sparkingshardamount.EGO;
                            }
                            break;
                        case "H":
                            if (value3.uptied == "2") { //ut2 or below
                                //console.log("value3.uptied = 2")
                                threadvalue += this.uptiethreadamount.EGOamount.H.from2to3.thread;
                            }
                            if (value3.uptied == "1") { //ut1 or don't hv
                                //console.log("value3.uptied = 1")
                                threadvalue += this.uptiethreadamount.EGOamount.H.from2to3.thread;
                                threadvalue += this.uptiethreadamount.EGOamount.H.from1to2.thread;
                            }
                            if (value3.uptied == "0") { //don't hv
                                //console.log("value3.uptied = 0")
                                threadvalue += this.uptiethreadamount.EGOamount.H.from2to3.thread;
                                threadvalue += this.uptiethreadamount.EGOamount.H.from1to2.thread;
                                shardvalue += this.uptiethreadamount.sparkingshardamount.EGO;
                            }
                            break;
                        case "Z":
                            if (key3 in this.ZEGOnotOriginal) { //not original
                                //console.log(key3);
                                if (value3.uptied == "2") { //ut2 or below
                                    //console.log("value3.uptied = 2")
                                    threadvalue += this.uptiethreadamount.EGOamount.ZnotOriginal.from2to3.thread;
                                }
                                if (value3.uptied == "1") { //ut1 or don't hv
                                    //console.log("value3.uptied = 1")
                                    threadvalue += this.uptiethreadamount.EGOamount.ZnotOriginal.from2to3.thread;
                                    threadvalue += this.uptiethreadamount.EGOamount.ZnotOriginal.from1to2.thread;
                                }
                                if (value3.uptied == "0") { //don't hv
                                    //console.log("value3.uptied = 0")
                                    threadvalue += this.uptiethreadamount.EGOamount.ZnotOriginal.from2to3.thread;
                                    threadvalue += this.uptiethreadamount.EGOamount.ZnotOriginal.from1to2.thread;
                                    shardvalue += this.uptiethreadamount.sparkingshardamount.EGO;
                                }
                            }
                            break;
                    }
                }
                this.CalResult.ThreadAmount += threadvalue;
                // console.log(key1, shardvalue);
                this.CalResult[key1] = shardvalue;
            }
        },
        calculate_case_ut3only(restore_data) {
            this.CalResult.ThreadAmount = 0
            for (const [key1, value1] of Object.entries(restore_data)) {
                // console.log(key1);      //this.CalResult.YiSang,this.CalResult.Faust....
                var identityIDList = value1;//this.All_IDs.YiSangIDs,this.All_IDs.FaustIDs....
                var shardvalue = 0;
                var threadvalue = 0;
                for (const [key2, value2] of Object.entries(identityIDList.IDs)) {
                    //key2 = Molar Office Fixer Outis,LCB Sinner Meursault...
                    //value2 = { rarity: "000", uptied: 0 },...
                    switch (value2.rarity) {
                        case "000":
                            if (value2.uptied == "2") { //ut2 or below
                                threadvalue += this.uptiethreadamount.IDamount.Rarity000.from2to3.thread;
                            }
                            if (value2.uptied == "1") { //ut1 or don't hv
                                threadvalue += this.uptiethreadamount.IDamount.Rarity000.from2to3.thread;
                                threadvalue += this.uptiethreadamount.IDamount.Rarity000.from1to2.thread;
                            }
                            break;
                        case "00":
                            if (value2.uptied == "2") { //ut2 or below
                                threadvalue += this.uptiethreadamount.IDamount.Rarity00.from2to3.thread;
                            }
                            if (value2.uptied == "1") { //ut1 or don't hv
                                threadvalue += this.uptiethreadamount.IDamount.Rarity00.from2to3.thread;
                                threadvalue += this.uptiethreadamount.IDamount.Rarity00.from1to2.thread;
                            }
                            break;
                        case "0": //do nothing as lcb sinner only do ut4
                            break;
                    }
                }
                for (const [key3, value3] of Object.entries(identityIDList.EGOs)) {
                    //key3 = Chains of Others,Regret...
                    //value3 = { rarity: "Z", uptied: 0 },...
                    //need to filter out the original EGOs for each Sinner
                    switch (value3.rarity) {
                        case "W":
                            if (value3.uptied == "2") { //ut2 or below
                                //console.log("value3.uptied = 2")
                                threadvalue += this.uptiethreadamount.EGOamount.W.from2to3.thread;
                            }
                            if (value3.uptied == "1") { //ut1 or don't hv
                                //console.log("value3.uptied = 1")
                                threadvalue += this.uptiethreadamount.EGOamount.W.from2to3.thread;
                                threadvalue += this.uptiethreadamount.EGOamount.W.from1to2.thread;
                            }
                            break;
                        case "T":
                            if (value3.uptied == "2") { //ut2 or below
                                //console.log("value3.uptied = 2")
                                threadvalue += this.uptiethreadamount.EGOamount.T.from2to3.thread;
                            }
                            if (value3.uptied == "1") { //ut1 or don't hv
                                //console.log("value3.uptied = 1")
                                threadvalue += this.uptiethreadamount.EGOamount.T.from2to3.thread;
                                threadvalue += this.uptiethreadamount.EGOamount.T.from1to2.thread;
                            }
                            break;
                        case "H":
                            if (value3.uptied == "2") { //ut2 or below
                                //console.log("value3.uptied = 2")
                                threadvalue += this.uptiethreadamount.EGOamount.H.from2to3.thread;
                            }
                            if (value3.uptied == "1") { //ut1 or don't hv
                                //console.log("value3.uptied = 1")
                                threadvalue += this.uptiethreadamount.EGOamount.H.from2to3.thread;
                                threadvalue += this.uptiethreadamount.EGOamount.H.from1to2.thread;
                            }
                            break;
                        case "Z":
                            if (key3 in this.ZEGOnotOriginal) { //not original
                                //console.log(key3);
                                if (value3.uptied == "2") { //ut2 or below
                                    //console.log("value3.uptied = 2")
                                    threadvalue += this.uptiethreadamount.EGOamount.ZnotOriginal.from2to3.thread;
                                }
                                if (value3.uptied == "1") { //ut1 or don't hv
                                    //console.log("value3.uptied = 1")
                                    threadvalue += this.uptiethreadamount.EGOamount.ZnotOriginal.from2to3.thread;
                                    threadvalue += this.uptiethreadamount.EGOamount.ZnotOriginal.from1to2.thread;
                                }
                            }
                            break;
                    }
                }
                this.CalResult.ThreadAmount += threadvalue;
                // console.log(key1, shardvalue);
                this.CalResult[key1] = shardvalue;
            }
        },
        calculate_case_ut4(restore_data) {
            this.CalResult.ThreadAmount = 0
            for (const [key1, value1] of Object.entries(restore_data)) {
                // console.log(key1);      //this.CalResult.YiSang,this.CalResult.Faust....
                var identityIDList = value1;//this.All_IDs.YiSangIDs,this.All_IDs.FaustIDs....
                var shardvalue = 0;
                var threadvalue = 0;
                for (const [key2, value2] of Object.entries(identityIDList.IDs)) {
                    //key2 = Molar Office Fixer Outis,LCB Sinner Meursault...
                    //value2 = { rarity: "000", uptied: 0 },...
                    switch (value2.rarity) {
                        case "000":
                            if (value2.uptied == "3") { //ut3
                                //console.log("value3.uptied = 2")
                                threadvalue += this.uptiethreadamount.IDamount.Rarity000.from3to4.thread;
                                shardvalue += this.uptiethreadamount.IDamount.Rarity000.from3to4.shard;
                            }
                            if (value2.uptied == "2") { //ut2 or below
                                threadvalue += this.uptiethreadamount.IDamount.Rarity000.from3to4.thread;
                                shardvalue += this.uptiethreadamount.IDamount.Rarity000.from3to4.shard;
                                threadvalue += this.uptiethreadamount.IDamount.Rarity000.from2to3.thread;
                            }
                            if (value2.uptied == "1") { //ut1 or don't hv
                                threadvalue += this.uptiethreadamount.IDamount.Rarity000.from3to4.thread;
                                shardvalue += this.uptiethreadamount.IDamount.Rarity000.from3to4.shard;
                                threadvalue += this.uptiethreadamount.IDamount.Rarity000.from2to3.thread;
                                threadvalue += this.uptiethreadamount.IDamount.Rarity000.from1to2.thread;
                            }
                            if (value2.uptied == "0") { //don't hv
                                threadvalue += this.uptiethreadamount.IDamount.Rarity000.from3to4.thread;
                                shardvalue += this.uptiethreadamount.IDamount.Rarity000.from3to4.shard;
                                threadvalue += this.uptiethreadamount.IDamount.Rarity000.from2to3.thread;
                                threadvalue += this.uptiethreadamount.IDamount.Rarity000.from1to2.thread;
                                shardvalue += this.uptiethreadamount.sparkingshardamount.Rarity000;
                            }
                            break;
                        case "00":
                            if (value2.uptied == "3") { //ut3
                                //console.log("value3.uptied = 2")
                                threadvalue += this.uptiethreadamount.IDamount.Rarity00.from3to4.thread;
                                shardvalue += this.uptiethreadamount.IDamount.Rarity00.from3to4.shard;
                            }
                            if (value2.uptied == "2") { //ut2 or below
                                threadvalue += this.uptiethreadamount.IDamount.Rarity00.from3to4.thread;
                                shardvalue += this.uptiethreadamount.IDamount.Rarity00.from3to4.shard;
                                threadvalue += this.uptiethreadamount.IDamount.Rarity00.from2to3.thread;
                            }
                            if (value2.uptied == "1") { //ut1 or don't hv
                                threadvalue += this.uptiethreadamount.IDamount.Rarity00.from3to4.thread;
                                shardvalue += this.uptiethreadamount.IDamount.Rarity00.from3to4.shard;
                                threadvalue += this.uptiethreadamount.IDamount.Rarity00.from2to3.thread;
                                threadvalue += this.uptiethreadamount.IDamount.Rarity00.from1to2.thread;
                            }
                            if (value2.uptied == "0") { //don't hv
                                threadvalue += this.uptiethreadamount.IDamount.Rarity00.from3to4.thread;
                                shardvalue += this.uptiethreadamount.IDamount.Rarity00.from3to4.shard;
                                threadvalue += this.uptiethreadamount.IDamount.Rarity00.from2to3.thread;
                                threadvalue += this.uptiethreadamount.IDamount.Rarity00.from1to2.thread;
                                shardvalue += this.uptiethreadamount.sparkingshardamount.Rarity00;
                            }
                            break;
                        case "0":
                            if (value2.uptied != "4") { //ut3 or below
                                //console.log("value3.uptied = 2")
                                threadvalue += this.uptiethreadamount.IDamount.Rarity0.from3to4.thread;
                                shardvalue += this.uptiethreadamount.IDamount.Rarity0.from3to4.shard;
                            }
                            break;
                    }
                }
                for (const [key3, value3] of Object.entries(identityIDList.EGOs)) {
                    //key3 = Chains of Others,Regret...
                    //value3 = { rarity: "Z", uptied: 0 },...
                    //need to filter out the original EGOs for each Sinner
                    switch (value3.rarity) {
                        case "W":
                            if (value3.uptied == "3") { //ut3
                                //console.log("value3.uptied = 2")
                                threadvalue += this.uptiethreadamount.EGOamount.W.from3to4.thread;
                                shardvalue += this.uptiethreadamount.EGOamount.W.from3to4.shard;
                            }
                            if (value3.uptied == "2") { //ut2 or below
                                //console.log("value3.uptied = 2")
                                threadvalue += this.uptiethreadamount.EGOamount.W.from3to4.thread;
                                shardvalue += this.uptiethreadamount.EGOamount.W.from3to4.shard;
                                threadvalue += this.uptiethreadamount.EGOamount.W.from2to3.thread;
                            }
                            if (value3.uptied == "1") { //ut1 or don't hv
                                //console.log("value3.uptied = 1")
                                threadvalue += this.uptiethreadamount.EGOamount.W.from3to4.thread;
                                shardvalue += this.uptiethreadamount.EGOamount.W.from3to4.shard;
                                threadvalue += this.uptiethreadamount.EGOamount.W.from2to3.thread;
                                threadvalue += this.uptiethreadamount.EGOamount.W.from1to2.thread;
                            }
                            if (value3.uptied == "0") { //don't hv
                                //console.log("value3.uptied = 0")
                                threadvalue += this.uptiethreadamount.EGOamount.W.from3to4.thread;
                                shardvalue += this.uptiethreadamount.EGOamount.W.from3to4.shard;
                                threadvalue += this.uptiethreadamount.EGOamount.W.from2to3.thread;
                                threadvalue += this.uptiethreadamount.EGOamount.W.from1to2.thread;
                                shardvalue += this.uptiethreadamount.sparkingshardamount.EGO;
                            }
                            break;
                        case "T":
                            if (value3.uptied == "3") { //ut3
                                //console.log("value3.uptied = 2")
                                threadvalue += this.uptiethreadamount.EGOamount.T.from3to4.thread;
                                shardvalue += this.uptiethreadamount.EGOamount.T.from3to4.shard;
                            }
                            if (value3.uptied == "2") { //ut2 or below
                                //console.log("value3.uptied = 2")
                                threadvalue += this.uptiethreadamount.EGOamount.T.from3to4.thread;
                                shardvalue += this.uptiethreadamount.EGOamount.T.from3to4.shard;
                                threadvalue += this.uptiethreadamount.EGOamount.T.from2to3.thread;
                            }
                            if (value3.uptied == "1") { //ut1 or don't hv
                                //console.log("value3.uptied = 1")
                                threadvalue += this.uptiethreadamount.EGOamount.T.from3to4.thread;
                                shardvalue += this.uptiethreadamount.EGOamount.T.from3to4.shard;
                                threadvalue += this.uptiethreadamount.EGOamount.T.from2to3.thread;
                                threadvalue += this.uptiethreadamount.EGOamount.T.from1to2.thread;
                            }
                            if (value3.uptied == "0") { //don't hv
                                //console.log("value3.uptied = 0")
                                threadvalue += this.uptiethreadamount.EGOamount.T.from3to4.thread;
                                shardvalue += this.uptiethreadamount.EGOamount.T.from3to4.shard;
                                threadvalue += this.uptiethreadamount.EGOamount.T.from2to3.thread;
                                threadvalue += this.uptiethreadamount.EGOamount.T.from1to2.thread;
                                shardvalue += this.uptiethreadamount.sparkingshardamount.EGO;
                            }
                            break;
                        case "H":
                            if (value3.uptied == "3") { //ut3
                                //console.log("value3.uptied = 2")
                                threadvalue += this.uptiethreadamount.EGOamount.H.from3to4.thread;
                                shardvalue += this.uptiethreadamount.EGOamount.H.from3to4.shard;
                            }
                            if (value3.uptied == "2") { //ut2 or below
                                //console.log("value3.uptied = 2")
                                threadvalue += this.uptiethreadamount.EGOamount.H.from3to4.thread;
                                shardvalue += this.uptiethreadamount.EGOamount.H.from3to4.shard;
                                threadvalue += this.uptiethreadamount.EGOamount.H.from2to3.thread;
                            }
                            if (value3.uptied == "1") { //ut1 or don't hv
                                //console.log("value3.uptied = 1")
                                threadvalue += this.uptiethreadamount.EGOamount.H.from3to4.thread;
                                shardvalue += this.uptiethreadamount.EGOamount.H.from3to4.shard;
                                threadvalue += this.uptiethreadamount.EGOamount.H.from2to3.thread;
                                threadvalue += this.uptiethreadamount.EGOamount.H.from1to2.thread;
                            }
                            if (value3.uptied == "0") { //don't hv
                                //console.log("value3.uptied = 0")
                                threadvalue += this.uptiethreadamount.EGOamount.H.from3to4.thread;
                                shardvalue += this.uptiethreadamount.EGOamount.H.from3to4.shard;
                                threadvalue += this.uptiethreadamount.EGOamount.H.from2to3.thread;
                                threadvalue += this.uptiethreadamount.EGOamount.H.from1to2.thread;
                                shardvalue += this.uptiethreadamount.sparkingshardamount.EGO;
                            }
                            break;
                        case "Z":
                            if (key3 in this.ZEGOnotOriginal) { //not original
                                //console.log(key3);
                                if (value3.uptied == "3") { //ut3
                                    //console.log("value3.uptied = 2")
                                    threadvalue += this.uptiethreadamount.EGOamount.ZnotOriginal.from3to4.thread;
                                    shardvalue += this.uptiethreadamount.EGOamount.ZnotOriginal.from3to4.shard;
                                }
                                if (value3.uptied == "2") { //ut2
                                    //console.log("value3.uptied = 2")
                                    threadvalue += this.uptiethreadamount.EGOamount.ZnotOriginal.from3to4.thread;
                                    shardvalue += this.uptiethreadamount.EGOamount.ZnotOriginal.from3to4.shard;
                                    threadvalue += this.uptiethreadamount.EGOamount.ZnotOriginal.from2to3.thread;
                                }
                                if (value3.uptied == "1") { //ut1
                                    //console.log("value3.uptied = 1")
                                    threadvalue += this.uptiethreadamount.EGOamount.ZnotOriginal.from3to4.thread;
                                    shardvalue += this.uptiethreadamount.EGOamount.ZnotOriginal.from3to4.shard;
                                    threadvalue += this.uptiethreadamount.EGOamount.ZnotOriginal.from2to3.thread;
                                    threadvalue += this.uptiethreadamount.EGOamount.ZnotOriginal.from1to2.thread;
                                }
                                if (value3.uptied == "0") { //don't hv
                                    //console.log("value3.uptied = 0")
                                    threadvalue += this.uptiethreadamount.EGOamount.ZnotOriginal.from3to4.thread;
                                    shardvalue += this.uptiethreadamount.EGOamount.ZnotOriginal.from3to4.shard;
                                    threadvalue += this.uptiethreadamount.EGOamount.ZnotOriginal.from2to3.thread;
                                    threadvalue += this.uptiethreadamount.EGOamount.ZnotOriginal.from1to2.thread;
                                    shardvalue += this.uptiethreadamount.sparkingshardamount.EGO;
                                }
                            } else {
                                if (value3.uptied != "4") { //ut2 or below
                                    //console.log("value3.uptied = 2")
                                    threadvalue += this.uptiethreadamount.EGOamount.Z.from3to4.thread;
                                    shardvalue += this.uptiethreadamount.EGOamount.Z.from3to4.shard;
                                }
                            }
                            break;
                    }
                }
                this.CalResult.ThreadAmount += threadvalue;
                // console.log(key1, shardvalue);
                this.CalResult[key1] = shardvalue;
            }
        },
        calculate_case_ut4only(restore_data) {
            this.CalResult.ThreadAmount = 0
            for (const [key1, value1] of Object.entries(restore_data)) {
                // console.log(key1);      //this.CalResult.YiSang,this.CalResult.Faust....
                var identityIDList = value1;//this.All_IDs.YiSangIDs,this.All_IDs.FaustIDs....
                var shardvalue = 0;
                var threadvalue = 0;
                for (const [key2, value2] of Object.entries(identityIDList.IDs)) {
                    //key2 = Molar Office Fixer Outis,LCB Sinner Meursault...
                    //value2 = { rarity: "000", uptied: 0 },...
                    switch (value2.rarity) {
                        case "000":
                            if (value2.uptied == "3") { //ut3
                                //console.log("value3.uptied = 2")
                                threadvalue += this.uptiethreadamount.IDamount.Rarity000.from3to4.thread;
                                shardvalue += this.uptiethreadamount.IDamount.Rarity000.from3to4.shard;
                            }
                            if (value2.uptied == "2") { //ut2 or below
                                threadvalue += this.uptiethreadamount.IDamount.Rarity000.from3to4.thread;
                                shardvalue += this.uptiethreadamount.IDamount.Rarity000.from3to4.shard;
                                threadvalue += this.uptiethreadamount.IDamount.Rarity000.from2to3.thread;
                            }
                            if (value2.uptied == "1") { //ut1 or don't hv
                                threadvalue += this.uptiethreadamount.IDamount.Rarity000.from3to4.thread;
                                shardvalue += this.uptiethreadamount.IDamount.Rarity000.from3to4.shard;
                                threadvalue += this.uptiethreadamount.IDamount.Rarity000.from2to3.thread;
                                threadvalue += this.uptiethreadamount.IDamount.Rarity000.from1to2.thread;
                            }
                            break;
                        case "00":
                            if (value2.uptied == "3") { //ut3
                                //console.log("value3.uptied = 2")
                                threadvalue += this.uptiethreadamount.IDamount.Rarity00.from3to4.thread;
                                shardvalue += this.uptiethreadamount.IDamount.Rarity00.from3to4.shard;
                            }
                            if (value2.uptied == "2") { //ut2 or below
                                threadvalue += this.uptiethreadamount.IDamount.Rarity00.from3to4.thread;
                                shardvalue += this.uptiethreadamount.IDamount.Rarity00.from3to4.shard;
                                threadvalue += this.uptiethreadamount.IDamount.Rarity00.from2to3.thread;
                            }
                            if (value2.uptied == "1") { //ut1 or don't hv
                                threadvalue += this.uptiethreadamount.IDamount.Rarity00.from3to4.thread;
                                shardvalue += this.uptiethreadamount.IDamount.Rarity00.from3to4.shard;
                                threadvalue += this.uptiethreadamount.IDamount.Rarity00.from2to3.thread;
                                threadvalue += this.uptiethreadamount.IDamount.Rarity00.from1to2.thread;
                            }
                            break;
                        case "0":
                            if (value2.uptied != "4") { //ut3 or below
                                //console.log("value3.uptied = 2")
                                threadvalue += this.uptiethreadamount.IDamount.Rarity0.from3to4.thread;
                                shardvalue += this.uptiethreadamount.IDamount.Rarity0.from3to4.shard;
                            }
                            break;
                    }
                }
                for (const [key3, value3] of Object.entries(identityIDList.EGOs)) {
                    //key3 = Chains of Others,Regret...
                    //value3 = { rarity: "Z", uptied: 0 },...
                    //need to filter out the original EGOs for each Sinner
                    switch (value3.rarity) {
                        case "W":
                            if (value3.uptied == "3") { //ut3
                                //console.log("value3.uptied = 2")
                                threadvalue += this.uptiethreadamount.EGOamount.W.from3to4.thread;
                                shardvalue += this.uptiethreadamount.EGOamount.W.from3to4.shard;
                            }
                            if (value3.uptied == "2") { //ut2 or below
                                //console.log("value3.uptied = 2")
                                threadvalue += this.uptiethreadamount.EGOamount.W.from3to4.thread;
                                shardvalue += this.uptiethreadamount.EGOamount.W.from3to4.shard;
                                threadvalue += this.uptiethreadamount.EGOamount.W.from2to3.thread;
                            }
                            if (value3.uptied == "1") { //ut1 or don't hv
                                //console.log("value3.uptied = 1")
                                threadvalue += this.uptiethreadamount.EGOamount.W.from3to4.thread;
                                shardvalue += this.uptiethreadamount.EGOamount.W.from3to4.shard;
                                threadvalue += this.uptiethreadamount.EGOamount.W.from2to3.thread;
                                threadvalue += this.uptiethreadamount.EGOamount.W.from1to2.thread;
                            }
                            break;
                        case "T":
                            if (value3.uptied == "3") { //ut3
                                //console.log("value3.uptied = 2")
                                threadvalue += this.uptiethreadamount.EGOamount.T.from3to4.thread;
                                shardvalue += this.uptiethreadamount.EGOamount.T.from3to4.shard;
                            }
                            if (value3.uptied == "2") { //ut2 or below
                                //console.log("value3.uptied = 2")
                                threadvalue += this.uptiethreadamount.EGOamount.T.from3to4.thread;
                                shardvalue += this.uptiethreadamount.EGOamount.T.from3to4.shard;
                                threadvalue += this.uptiethreadamount.EGOamount.T.from2to3.thread;
                            }
                            if (value3.uptied == "1") { //ut1 or don't hv
                                //console.log("value3.uptied = 1")
                                threadvalue += this.uptiethreadamount.EGOamount.T.from3to4.thread;
                                shardvalue += this.uptiethreadamount.EGOamount.T.from3to4.shard;
                                threadvalue += this.uptiethreadamount.EGOamount.T.from2to3.thread;
                                threadvalue += this.uptiethreadamount.EGOamount.T.from1to2.thread;
                            }
                            break;
                        case "H":
                            if (value3.uptied == "3") { //ut3
                                //console.log("value3.uptied = 2")
                                threadvalue += this.uptiethreadamount.EGOamount.H.from3to4.thread;
                                shardvalue += this.uptiethreadamount.EGOamount.H.from3to4.shard;
                            }
                            if (value3.uptied == "2") { //ut2 or below
                                //console.log("value3.uptied = 2")
                                threadvalue += this.uptiethreadamount.EGOamount.H.from3to4.thread;
                                shardvalue += this.uptiethreadamount.EGOamount.H.from3to4.shard;
                                threadvalue += this.uptiethreadamount.EGOamount.H.from2to3.thread;
                            }
                            if (value3.uptied == "1") { //ut1 or don't hv
                                //console.log("value3.uptied = 1")
                                threadvalue += this.uptiethreadamount.EGOamount.H.from3to4.thread;
                                shardvalue += this.uptiethreadamount.EGOamount.H.from3to4.shard;
                                threadvalue += this.uptiethreadamount.EGOamount.H.from2to3.thread;
                                threadvalue += this.uptiethreadamount.EGOamount.H.from1to2.thread;
                            }
                            break;
                        case "Z":
                            if (key3 in this.ZEGOnotOriginal) { //not original
                                //console.log(key3);
                                if (value3.uptied == "3") { //ut3
                                    //console.log("value3.uptied = 2")
                                    threadvalue += this.uptiethreadamount.EGOamount.ZnotOriginal.from3to4.thread;
                                    shardvalue += this.uptiethreadamount.EGOamount.ZnotOriginal.from3to4.shard;
                                }
                                if (value3.uptied == "2") { //ut2
                                    //console.log("value3.uptied = 2")
                                    threadvalue += this.uptiethreadamount.EGOamount.ZnotOriginal.from3to4.thread;
                                    shardvalue += this.uptiethreadamount.EGOamount.ZnotOriginal.from3to4.shard;
                                    threadvalue += this.uptiethreadamount.EGOamount.ZnotOriginal.from2to3.thread;
                                }
                                if (value3.uptied == "1") { //ut1
                                    //console.log("value3.uptied = 1")
                                    threadvalue += this.uptiethreadamount.EGOamount.ZnotOriginal.from3to4.thread;
                                    shardvalue += this.uptiethreadamount.EGOamount.ZnotOriginal.from3to4.shard;
                                    threadvalue += this.uptiethreadamount.EGOamount.ZnotOriginal.from2to3.thread;
                                    threadvalue += this.uptiethreadamount.EGOamount.ZnotOriginal.from1to2.thread;
                                }
                            } else {
                                if (value3.uptied != "4") { //ut2 or below
                                    //console.log("value3.uptied = 2")
                                    threadvalue += this.uptiethreadamount.EGOamount.Z.from3to4.thread;
                                    shardvalue += this.uptiethreadamount.EGOamount.Z.from3to4.shard;
                                }
                            }
                            break;
                    }
                }
                this.CalResult.ThreadAmount += threadvalue;
                // console.log(key1, shardvalue);
                this.CalResult[key1] = shardvalue;
            }
        },
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
                        this.calculate_case_ut3only(restore_data);
                        break;
                    case 'uptie4':
                        this.calculate_case_ut4(restore_data);
                        break;
                    case 'uptie4only':
                        this.calculate_case_ut4only(restore_data);
                        break;
                    case 'uptie5':
                        this.calculate_case_ut5(restore_data);
                        break;
                    case 'uptie5only':
                        this.calculate_case_ut5only(restore_data);
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
    width: min(50px, 8vw);
}
</style>