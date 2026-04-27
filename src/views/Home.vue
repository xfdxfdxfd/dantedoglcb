<template>
    <div class="page-shell">
        <section class="page-grid">
            <div class="content-card overflow-hidden">
                <div class="hero-grid px-6 py-8 md:px-8 md:py-10">
                    <div class="hero-card">
                        <div class="deco-heading-block lg:text-left">
                            <p class="section-kicker">{{ $t(`HomePlannerLabel`) }}</p>
                            <div class="deco-divider mt-4 lg:mx-0 lg:justify-start">{{ $t(`HomeGrandRegister`) }}</div>
                        </div>
                        <h1 class="section-title mt-6 max-w-3xl">{{ $t(`Welcome`) }}</h1>
                        <p class="mt-4 max-w-2xl text-lg leading-8 text-stone-300">{{ $t(`WelcomeText`) }}</p>
                        <div class="mt-8 panel-divider"></div>
                        <h2 class="mt-8 font-accent text-2xl uppercase tracking-[0.18em] text-gold md:text-3xl">{{ $t(`WelcomeTitle`) }}</h2>
                        <p class="section-copy mt-4 max-w-3xl">{{ $t(`WelcomeParagraph`) }}</p>
                    </div>

                    <div class="hero-card">
                        <div class="deco-heading-block">
                            <p class="section-kicker">{{ $t(`HomeQuickFlow`) }}</p>
                            <div class="deco-divider mt-4">{{ $t(`HomeThreeActs`) }}</div>
                        </div>
                        <div class="mt-5 space-y-5">
                            <article class="muted-panel p-5">
                                <div class="flex items-start gap-4">
                                    <span class="deco-diamond mt-1" aria-hidden="true"><span class="deco-number">I</span></span>
                                    <div>
                                        <h3 class="font-accent text-lg uppercase tracking-[0.18em] text-white">{{ $t(`StatusSetting`) }}</h3>
                                        <p class="mt-2 text-sm leading-7 text-stone-300">{{ $t(`statusSettingHomepage`) }}</p>
                                    </div>
                                </div>
                            </article>
                            <article class="muted-panel p-5">
                                <div class="flex items-start gap-4">
                                    <span class="deco-diamond mt-1" aria-hidden="true"><span class="deco-number">II</span></span>
                                    <div>
                                        <h3 class="font-accent text-lg uppercase tracking-[0.18em] text-white">{{ $t(`UptieCalculator`) }}</h3>
                                        <p class="mt-2 text-sm leading-7 text-stone-300">{{ $t(`uptieCalculatorHomepage`) }}</p>
                                    </div>
                                </div>
                            </article>
                            <article class="muted-panel p-5">
                                <div class="flex items-start gap-4">
                                    <span class="deco-diamond mt-1" aria-hidden="true"><span class="deco-number">III</span></span>
                                    <div>
                                        <h3 class="font-accent text-lg uppercase tracking-[0.18em] text-white">{{ $t(`ExpCalculator`) }}</h3>
                                        <p class="mt-2 text-sm leading-7 text-stone-300">{{ $t(`ExpCalculatorHomepage`) }}</p>
                                    </div>
                                </div>
                            </article>
                        </div>
                    </div>
                </div>

                <div class="border-t border-white/10 px-6 py-8 md:px-8">
                    <p class="section-kicker">{{ $t(`HomeConnect`) }}</p>
                    <div class="deco-divider mt-4 justify-start">{{ $t(`HomeSalon`) }}</div>
                    <h2 class="mt-4 font-accent text-2xl uppercase tracking-[0.18em] text-white">{{ $t(`ContactTitle`) }}</h2>
                    <p class="mt-3 max-w-3xl text-sm leading-7 text-stone-300">{{ $t(`ContactParagraph`) }}</p>

                    <div class="mt-6 flex flex-wrap gap-4">
                        <a href="https://discord.gg/UdFrGmKfqE" class="deco-image-frame transition hover:border-gold hover:shadow-glow">
                            <img class="h-12 w-auto grayscale transition hover:grayscale-0" alt="Discord" src="../../src/assets/DanteLogoDiscord.webp">
                        </a>
                        <a href="https://github.com/xfdxfdxfd/dantedoglcb" class="deco-image-frame transition hover:border-gold hover:shadow-glow">
                            <img class="h-12 w-auto grayscale transition hover:grayscale-0" alt="GitHub" src="../../src/assets/DanteLogoGithub.webp">
                        </a>
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>

<script>

export default {
    name: 'Home',
}
</script>