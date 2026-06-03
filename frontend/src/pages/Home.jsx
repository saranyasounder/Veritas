import { Link } from 'react-router-dom'
import { useEffect, useRef } from 'react'

const Home = () => {
    return (
        <div className="relative min-h-screen overflow-hidden">

            {/* floating orbs */}
            <div className="orb orb-green" style={{ top: '-100px', right: '10%' }} />
            <div className="orb orb-teal" style={{ top: '300px', left: '5%' }} />

            {/* hero section */}
<div className="relative z-10 flex flex-col items-center text-center py-24 gap-6">

    {/* VERITAS watermark */}
    <div
        className="absolute inset-0 flex items-center justify-center pointer-events-none select-none"
        style={{
            fontSize: 'clamp(80px, 20vw, 240px)',
            fontWeight: 900,
            letterSpacing: '-0.05em',
            background: 'linear-gradient(135deg, rgba(34,197,94,0.06), rgba(20,184,166,0.06))',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
            zIndex: 0,
        }}
    >
        VERITAS
    </div>

    {/* rest of hero content stays exactly the same, just add z-10 */}
    <div className="relative z-10 flex flex-col items-center gap-6">
        
        {/* badge */}
        <div className="glass-card px-4 py-2 text-xs font-medium text-green-400 glow-border">
            LLM Evaluation & Benchmarking Platform
        </div>

        {/* headline */}
        <h1 className="text-6xl font-bold leading-tight max-w-3xl">
            Evaluate AI Models with{' '}
            <span className="gradient-text">Precision</span>
        </h1>

        {/* subheadline */}
        <p className="text-gray-400 text-lg max-w-xl leading-relaxed">
            Benchmark large language models across accuracy, hallucination detection,
            semantic similarity, and reasoning quality — all in one platform.
        </p>

        {/* CTA buttons */}
        <div className="flex gap-4 mt-4">
            <Link to="/evaluate">
                <button className="gradient-btn px-8 py-3 text-sm">
                    Start Evaluating
                </button>
            </Link>
            <Link to="/results">
                <button className="glass-card px-8 py-3 text-sm text-gray-300 hover:text-white cursor-pointer">
                    View Results
                </button>
            </Link>
        </div>
    </div>
</div>

            {/* metrics overview cards */}
            <div className="relative z-10 grid grid-cols-2 md:grid-cols-4 gap-4 mb-16">
                {[
                    { label: 'BLEU Score', desc: 'Word overlap precision' },
                    { label: 'BERTScore', desc: 'Semantic similarity' },
                    { label: 'Hallucination', desc: 'Factual grounding'},
                    { label: 'LLM Judge', desc: 'Qualitative scoring'},
                ].map((metric) => (
                    <div key={metric.label} className="glass-card p-6 flex flex-col gap-2">
                        <span className="text-2xl">{metric.icon}</span>
                        <p className="text-sm font-semibold text-white">{metric.label}</p>
                        <p className="text-xs text-gray-400">{metric.desc}</p>
                    </div>
                ))}
            </div>

            {/* how it works */}
            <div className="relative z-10 mb-16">
                <h2 className="text-2xl font-bold text-center mb-8">
                    How it <span className="gradient-text">works</span>
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {[
                        {
                            step: '01',
                            title: 'Submit a prompt',
                            desc: 'Enter your prompt, select a model, and optionally provide a reference answer and source document.'
                        },
                        {
                            step: '02',
                            title: 'Run evaluation',
                            desc: 'Veritas calls the model, runs all metrics in parallel, and scores the response across multiple dimensions.'
                        },
                        {
                            step: '03',
                            title: 'Analyze results',
                            desc: 'View detailed scores, compare models side by side, and track performance over time.'
                        },
                    ].map((item) => (
                        <div key={item.step} className="glass-card p-6 flex flex-col gap-3">
                            <span className="text-3xl font-bold gradient-text">{item.step}</span>
                            <p className="font-semibold text-white">{item.title}</p>
                            <p className="text-sm text-gray-400 leading-relaxed">{item.desc}</p>
                        </div>
                    ))}
                </div>
            </div>

        </div>
    )
}

export default Home