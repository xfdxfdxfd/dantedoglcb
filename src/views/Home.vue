<template>
    <div style="min-height: 100vh;" class="content">
        <div style="position: relative;">
            <div class="box1">
                <h1 style="font-size: 40px;padding-top: 20px;color: #ffffff;">{{ $t(`Welcome`) }}</h1>
                <h2 style="color: #c2bfbf;">{{ $t(`WelcomeText`) }}</h2>
                &nbsp;
                <h2 style="border-bottom: 3px solid rgb(172, 172, 172);"></h2>
                &nbsp;
                <h2 style="white-space: pre-line;padding:10px;color:rgb(255, 220, 161);font-size: 35px;">
                    {{ $t(`WelcomeTitle`) }}</h2>
                <h3 style="white-space: pre-line;color:#c2bfbf">{{ $t(`WelcomeParagraph`) }}</h3>
                &nbsp;
                <h2 class="box1h2text">1. {{ $t(`StatusSetting`) }}</h2>
                <h3 class="box1h3text">{{ $t(`StatusSettingSection`) }}</h3>
                &nbsp;
                <h2 class="box1h2text">2. {{ $t(`UptieCalculator`) }}</h2>
                <h3 class="box1h3text">{{ $t(`UptieCalculatorSection1`) }}</h3>
                &nbsp;
                <h2 class="box1h2text">{{ $t(`ContactTitle`) }}</h2>
                <h3 class="box1h3text" style="margin-bottom: 10px;">{{ $t(`ContactParagraph`) }}</h3>
                <a href="https://discord.gg/UdFrGmKfqE">
                    <img style="margin: 0px;padding:0px;width: 150px;" class="pagetitle" alt="LC Dog Dante"
                        src="../../src/assets/DanteLogoDiscord.webp">
                </a>
                &nbsp;
                <a href="https://github.com/xfdxfdxfd/dantedoglcb">
                    <img style="margin: 0px;padding:0px;width: 150px;" class="pagetitle" alt="LC Dog Dante"
                        src="../../src/assets/DanteLogoGithub.webp">
                </a>
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
    watch: {
    }
}
</script>

<style>
.box1 {
    background-color: #000;
    color: #fff;
    background-color: rgba(255, 255, 255, 0.3);
    text-align: center;
    margin-top: max(100px, 10vh);
    margin-left: 5vw;
    margin-right: 5vw;
    border-radius: 25px;
}

.box1h2text {
    white-space: pre-line;
    color: #ffffff;
    font-size: 25px;
    padding-left: 3vw;
    padding-right: 3vw;

}

.box1h3text {
    white-space: pre-line;
    color: #ffffff;
    padding-left: 5vw;
    padding-right: 5vw;
}
</style>