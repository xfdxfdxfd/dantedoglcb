<template>
    <div style="min-height: 100vh">
        <div style="position: relative;padding-top: 70px;">
            <div class="box box1">
                <h1 style="font-size: 40px;padding-top: 20px;color: #ffffff;">{{$t(`Welcome`)}}</h1>
                <h2 style="color: #c2bfbf;">{{$t(`WelcomeText`)}}</h2>
                &nbsp;
                <h2 style="border-bottom: 3px solid rgb(172, 172, 172);"></h2>
                &nbsp;
                <h2 style="white-space: pre-line;padding:10px;color:#ffffff;font-size: 35px;">{{$t(`WelcomeTitle`)}}</h2>
                <h3 style="white-space: pre-line;color:#ffffff">{{$t(`WelcomeParagraph`)}}</h3>
                
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
</style>