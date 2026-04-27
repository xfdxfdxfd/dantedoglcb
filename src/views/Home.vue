<template>
    <div class="page-shell">
        <section class="mx-auto max-w-7xl px-4 py-8 md:px-6 lg:px-8">
            <div class="content-card overflow-hidden">
                <div class="grid gap-8 px-6 py-8 md:px-8 lg:grid-cols-[1.3fr_0.9fr] lg:items-start">
                    <div>
                        <p class="field-label text-gold">Limbus Company Planner</p>
                        <h1 class="section-title mt-3 max-w-3xl">{{ $t(`Welcome`) }}</h1>
                        <p class="mt-4 text-lg text-stone-300">{{ $t(`WelcomeText`) }}</p>
                        <div class="mt-6 panel-divider"></div>
                        <h2 class="mt-6 text-3xl font-bold text-gold">{{ $t(`WelcomeTitle`) }}</h2>
                        <p class="section-copy mt-4">{{ $t(`WelcomeParagraph`) }}</p>
                    </div>

                    <div class="rounded-[2rem] border border-white/10 bg-black/20 p-6">
                        <p class="field-label">Quick Flow</p>
                        <div class="mt-5 space-y-5">
                            <article class="rounded-2xl border border-white/10 bg-white/5 p-4">
                                <h3 class="text-xl font-semibold text-white">1. {{ $t(`StatusSetting`) }}</h3>
                                <p class="mt-2 text-sm leading-6 text-stone-300">{{ $t(`statusSettingHomepage`) }}</p>
                            </article>
                            <article class="rounded-2xl border border-white/10 bg-white/5 p-4">
                                <h3 class="text-xl font-semibold text-white">2. {{ $t(`UptieCalculator`) }}</h3>
                                <p class="mt-2 text-sm leading-6 text-stone-300">{{ $t(`uptieCalculatorHomepage`) }}</p>
                            </article>
                            <article class="rounded-2xl border border-white/10 bg-white/5 p-4">
                                <h3 class="text-xl font-semibold text-white">3. {{ $t(`ExpCalculator`) }}</h3>
                                <p class="mt-2 text-sm leading-6 text-stone-300">{{ $t(`ExpCalculatorHomepage`) }}</p>
                            </article>
                        </div>
                    </div>
                </div>

                <div class="border-t border-white/10 px-6 py-8 md:px-8">
                    <h2 class="text-2xl font-bold text-white">{{ $t(`ContactTitle`) }}</h2>
                    <p class="mt-3 max-w-3xl text-sm leading-7 text-stone-300">{{ $t(`ContactParagraph`) }}</p>

                    <div class="mt-6 flex flex-wrap gap-4">
                        <a href="https://discord.gg/UdFrGmKfqE" class="rounded-2xl border border-white/10 bg-black/20 p-4 transition hover:border-gold/60 hover:bg-white/5">
                            <img class="h-12 w-auto" alt="Discord" src="../../src/assets/DanteLogoDiscord.webp">
                        </a>
                        <a href="https://github.com/xfdxfdxfd/dantedoglcb" class="rounded-2xl border border-white/10 bg-black/20 p-4 transition hover:border-gold/60 hover:bg-white/5">
                            <img class="h-12 w-auto" alt="GitHub" src="../../src/assets/DanteLogoGithub.webp">
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