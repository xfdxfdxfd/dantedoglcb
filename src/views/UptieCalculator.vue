<template>
    <div style="min-height: 100vh;" class="content">
        <div style="position: relative;">
            <div class="box box1">
                <h1 style="font-size: 40px;padding-top: 20px;color: #ffffff;">{{$t(`UptieCalculator`)}}</h1>
                &nbsp;
                <h2 style="border-bottom: 3px solid rgb(172, 172, 172);"></h2>
                &nbsp;
                <h3 class="box1h3text">{{$t(`UptieCalculatorSection`)}}</h3>
                &nbsp;
                <h3 class="box1h3text" style="text-align:left;">{{$t(`You need`)}}:</h3>
                <h2 class="box1h2text">
                    <div style="padding-right: 570px">
                        <img class="shardimg" alt="ThreadAmount" src="../../src/assets/icon_twine.png">:{{ThreadAmount}}&nbsp;&nbsp;&nbsp;&nbsp;
                    </div>
                    &nbsp;
                    <div>
                        <img class="shardimg" alt="YiSangShard" src="../../src/assets/icon_piece-501YiSang.png">:{{YiSang}}&nbsp;&nbsp;&nbsp;&nbsp;
                        <img class="shardimg" alt="FaustShard" src="../../src/assets/icon_piece-502Faust.png">:{{Faust}}&nbsp;&nbsp;&nbsp;&nbsp;
                        <img class="shardimg" alt="DonShard" src="../../src/assets/icon_piece-503DonQuixote.png">:{{Don}}&nbsp;&nbsp;&nbsp;&nbsp;
                        <img class="shardimg" alt="RyoshuShard" src="../../src/assets/icon_piece-504Ryoshu.png">:{{Ryoshu}}&nbsp;&nbsp;&nbsp;&nbsp;
                        <img class="shardimg" alt="MeurShard" src="../../src/assets/icon_piece-505Meursault.png">:{{Meur}}&nbsp;&nbsp;&nbsp;&nbsp;
                        <img class="shardimg" alt="HongLuShard" src="../../src/assets/icon_piece-506HongLu.png">:{{HongLu}}&nbsp;&nbsp;&nbsp;&nbsp;
                    </div>
                    &nbsp;
                    <div>
                        <img class="shardimg" alt="HeathShard" src="../../src/assets/icon_piece-507Heathcliff.png">:{{Heath}}&nbsp;&nbsp;&nbsp;&nbsp;
                        <img class="shardimg" alt="IshShard" src="../../src/assets/icon_piece-508Ishmael.png">:{{Ish}}&nbsp;&nbsp;&nbsp;&nbsp;
                        <img class="shardimg" alt="RodionShard" src="../../src/assets/icon_piece-509Rodion.png">:{{Rodion}}&nbsp;&nbsp;&nbsp;&nbsp;
                        <img class="shardimg" alt="SinclairShard" src="../../src/assets/icon_piece-510EmilSinclair.png">:{{Sinclair}}&nbsp;&nbsp;&nbsp;&nbsp;
                        <img class="shardimg" alt="OutisShard" src="../../src/assets/icon_piece-511Outis.png">:{{Outis}}&nbsp;&nbsp;&nbsp;&nbsp;
                        <img class="shardimg" alt="GregorShard" src="../../src/assets/icon_piece-512Gregor.png">:{{Gregor}}&nbsp;&nbsp;&nbsp;&nbsp;
                    </div>
                    &nbsp;
                </h2>
            </div>
        </div>
    </div>
</template>

<script>

// import LimbusCompany from './components/LimbusCompany.vue'

export default {
  name: 'UptieCalculator',
  data(){
    return {
        ThreadAmount:0,
        YiSang: 0,
        Faust:0,
        Don:0,
        Ryoshu:0,
        Meur:0,
        HongLu:0,
        Heath:0,
        Rodion:0,
        Ish:0,
        Sinclair:0,
        Outis:0,
        Gregor:0,

    }
  },
  computed: {
  },
  methods: {
  },
  components: {
  },
  watch:{
  }
}
</script>

<style>
.shardimg{
    width:50px
}
</style>