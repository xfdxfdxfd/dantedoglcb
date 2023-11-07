<template>
    <div style="min-height: 100vh">
        <div style="position: relative;padding-top: 70px;">
            <div class="box box1">
                <h1 style="font-size: 40px;padding-top: 20px;color: #ffffff;">{{$t(`Welcome`)}}</h1>
                <h2 style="color: #c2bfbf;">{{$t(`WelcomeText`)}}</h2>
                &nbsp;
                <h2 style="border-bottom: 3px solid rgb(172, 172, 172);"></h2>
                &nbsp;
                <h2 style="white-space: pre-line;padding:10px;color:rgb(255, 220, 161);font-size: 35px;">{{$t(`WelcomeTitle`)}}</h2>
                <h3 style="white-space: pre-line;color:#c2bfbf">{{$t(`WelcomeParagraph`)}}</h3>
                &nbsp;
                <h2 class="box1h2text">1. {{$t(`UptieCalculator`)}}</h2>
                <h3 class="box1h3text">{{$t(`Welcomesection1`)}}</h3>
                &nbsp;
                <h2 class="box1h2text">{{$t(`ContactTitle`)}}</h2>
                <h3 class="box1h3text">{{$t(`ContactParagraph`)}}</h3>
                &nbsp;
            </div>
        </div>
    </div>
</template>

<script>

export default {
  name: 'Home',
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
.box1 {
    background-color: #000;
    color: #fff;
    background-color: rgba(255,255,255,0.3);
    text-align:center;
    margin:100px;
    border-radius: 25px;
  }
.box1h2text {
    white-space: pre-line;
    color:#ffffff;
    font-size: 28px;
}
.box1h3text {
    white-space: pre-line;
    color:#ffffff;
    padding-left: 100px;
    padding-right: 100px;
}
</style>