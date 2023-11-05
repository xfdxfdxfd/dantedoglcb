<template>
    <div style="height: 100vh;">
        <h1 style="padding: 20px;text-align: center;border-bottom: 3px solid #333;">{{$t(`Welcome`)}}</h1>
        <div class="wrapper">
            <div class="box box1">
                <h1 style="font-size: 32px;padding:10px;">No Dante can escape from grinding</h1>
                &nbsp;
                <h3 style="white-space: pre-line;">{{$t(`WelcomeText`)}}</h3>
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