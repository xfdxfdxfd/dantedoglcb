<template>
    <div style="height: 100vh;">
        <h1 style="padding: 20px;text-align: center;border-bottom: 3px solid #333;">{{$t(`Welcome`)}}</h1>
        <div class="wrapper">
            <div class="box box1">
                <h1 style="font-size: 40px;padding:10px;">{{$t(`WelcomeTitle`)}}</h1>
                <h2>{{$t(`WelcomeText`)}}</h2>
                <h3 style="white-space: pre-line;padding:10px;border-top: 3px solid rgb(172, 172, 172);">{{$t(`WelcomeParagraph`)}}</h3>
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