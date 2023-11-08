<template>
    <div style="min-height: 100vh;" class="content">
        <div style="position: relative;">
            <div class="box box1">
                <h1 style="font-size: 40px;padding-top: 20px;color: #ffffff;">{{$t(`StatusSetting`)}}</h1>
                &nbsp;
                <h2 style="border-bottom: 3px solid rgb(172, 172, 172);"></h2>
                &nbsp;
                <button>Testing</button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
  name: 'StatusSetting',
  data(){
    return {
        IDs: {
            YiSangIDs: {
                "LCB YiSang":{rarity:"0",uptie:0,owned:false},
                "7 YiSang":{rarity:"00",uptie:0,owned:false},
                "Flower YiSang":{rarity:"000",uptie:0,owned:false},
            },
        }

    }
  },
  computed: {
  },
  methods: {
    testing(){
        console.log(this.IDs.YiSangIDs)
    }
  },
  components: {
  },
  watch:{
  }
}
</script>

<style></style>