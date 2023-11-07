<template>
    <div style="min-height: 100vh">
        <div style="position: relative;padding-top: 70px;">
            <div class="box box1">
                <h1 style="font-size: 40px;padding-top: 20px;color: #ffffff;">{{$t(`UptieCalculator`)}}</h1>
                &nbsp;
                <h2 style="border-bottom: 3px solid rgb(172, 172, 172);"></h2>
                &nbsp;
                <h3 class="box1h3text">{{$t(`Welcomesection1`)}}</h3>
                &nbsp;
                <h3 class="box1h3text" style="text-align:left;">{{$t(`You need`)}}:</h3>
                &nbsp;
                <h3 class="box1h3text">:{{ThreadAmount}}</h3>
                <h3 class="box1h3text">:{{YiSang}}</h3>
                <h3 class="box1h3text">:{{Faust}}</h3>
                <h3 class="box1h3text">:{{Don}}</h3>
                <h3 class="box1h3text">:{{Ryoshu}}</h3>
                <h3 class="box1h3text">:{{Meur}}</h3>
                <h3 class="box1h3text">:{{HongLu}}</h3>
                <h3 class="box1h3text">:{{Heath}}</h3>
                <h3 class="box1h3text">:{{Rodion}}</h3>
                <h3 class="box1h3text">:{{Ish}}</h3>
                <h3 class="box1h3text">:{{Sinclair}}</h3>
                <h3 class="box1h3text">:{{Outis}}</h3>
                <h3 class="box1h3text">:{{Gregor}}</h3>
            </div>
        </div>
    </div>
</template>

<script>

// import LimbusCompany from './components/LimbusCompany.vue'

export default {
  name: 'UptieCalculator',
  props: {
    name: String,
    Amount: Number
  },
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

<style></style>