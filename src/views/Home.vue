<template>
    <div class="content">
        <div>
            <div class="box box1">
                <h1 class="subtitle">{{ $t(`Welcome`) }}</h1>
                <h2 style="color: #c2bfbf;font-size:1.25rem">{{ $t(`WelcomeText`) }}</h2>
                &nbsp;
                <h2 class="separator"></h2>
                &nbsp;
                <h2 class="welcomeparagraph_yellow">{{ $t(`WelcomeTitle`) }}</h2>
                <h3 class="box1h3text" style="color:#c2bfbf">{{ $t(`WelcomeParagraph`) }}</h3>
                &nbsp;
                <h2 class="box1h2text">1. {{ $t(`StatusSetting`) }}</h2>
                <h3 class="box1h3text" style="color:#c2bfbf">{{ $t(`statusSettingHomepage`) }}</h3>
                &nbsp;
                <h2 class="box1h2text">2. {{ $t(`UptieCalculator`) }}</h2>
                <h3 class="box1h3text" style="color:#c2bfbf">{{ $t(`uptieCalculatorHomepage`) }}</h3>
                &nbsp;
                <h2 class="box1h2text">3. {{ $t(`ExpCalculator`) }}</h2>
                <h3 class="box1h3text" style="color:#c2bfbf">{{ $t(`ExpCalculatorHomepage`) }}</h3>
                &nbsp;
                <h2 class="box1h2text">{{ $t(`ContactTitle`) }}</h2>
                <h3 class="box1h3text" style="margin-bottom: 10px;color:#c2bfbf;">{{ $t(`ContactParagraph`) }}</h3>
                <a href="https://discord.gg/UdFrGmKfqE">
                    <img class="pagetitle" alt="LC Dog Dante" src="../../src/assets/DanteLogoDiscord.webp">
                </a>
                &nbsp;
                <a href="https://github.com/xfdxfdxfd/dantedoglcb">
                    <img class="pagetitle" alt="LC Dog Dante" src="../../src/assets/DanteLogoGithub.webp">
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
    mounted() {
    }
}
</script>

<style>
@import '../components/format.css';
</style>