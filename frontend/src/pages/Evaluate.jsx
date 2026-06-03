import { useState } from 'react'
import { evaluateModel } from '../services/api'
import LoadingSpinner from '../components/shared/LoadingSpinner'

const MODELS = [
    { id: 'openai/gpt-3.5-turbo', label: 'GPT-3.5 Turbo' },
    { id: 'openai/gpt-4o', label: 'GPT-4o' },
    { id: 'anthropic/claude-sonnet-4', label: 'Claude Sonnet 4' },
    { id: 'google/gemini-pro', label: 'Gemini Pro' },
]

const Toggle = ({ label, sublabel, enabled, onToggle }) => (
    <div className="flex items-center justify-between">
        <div>
            <p className="text-sm font-medium text-gray-300">{label}</p>
            <p className="text-xs text-gray-500 mt-0.5">{sublabel}</p>
        </div>
        <button
            onClick={onToggle}
            className="relative w-12 h-6 rounded-full transition-all duration-300 focus:outline-none"
            style={{
                background: enabled
                    ? 'linear-gradient(135deg, #22c55e, #14b8a6)'
                    : 'rgba(255,255,255,0.1)'
            }}
        >
            <div
                className="absolute top-0.5 w-5 h-5 bg-white rounded-full shadow transition-all duration-300"
                style={{ left: enabled ? '26px' : '2px' }}
            />
        </button>
    </div>
)

const Evaluate = () => {
    const [form, setForm] = useState({
        prompt: '',
        model_id: 'openai/gpt-3.5-turbo',
        reference: '',
        source: '',
    })
    const [autoReference, setAutoReference] = useState(true)
    const [autoSource, setAutoSource] = useState(true)
    const [loading, setLoading] = useState(false)
    const [result, setResult] = useState(null)
    const [error, setError] = useState(null)

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value })
    }

    const handleSubmit = async () => {
        if (!form.prompt) return
        setLoading(true)
        setError(null)
        setResult(null)

       try {
    const data = await evaluateModel({
        prompt: form.prompt,
        model_id: form.model_id,
        reference: autoReference ? null : form.reference || null,
        source: autoSource ? null : form.source || null,
    })
    setResult(data)
} catch (err) {
    setError('Evaluation failed. Please try again.')
} finally {
    setLoading(false)
}
    }

    const getScoreColor = (score) => {
        if (score >= 0.8) return '#22c55e'
        if (score >= 0.5) return '#f59e0b'
        return '#ef4444'
    }

    return (
        <div className="relative min-h-screen">
            <div className="orb orb-green" style={{ top: '100px', right: '5%' }} />
            <div className="orb orb-teal" style={{ bottom: '100px', left: '5%' }} />

            <div className="relative z-10 max-w-3xl mx-auto py-12">

                {/* header */}
                <div className="mb-10">
                    <h1 className="text-4xl font-bold mb-2">
                        Run an <span className="gradient-text">Evaluation</span>
                    </h1>
                    <p className="text-gray-400">
                        Submit a prompt and evaluate how well a model responds across multiple quality dimensions.
                    </p>
                </div>

                {/* form */}
                <div className="glass-card p-8 flex flex-col gap-6">

                    {/* prompt */}
                    <div className="flex flex-col gap-2">
                        <label className="text-sm font-medium text-gray-300">
                            Prompt <span className="text-green-400">*</span>
                        </label>
                        <textarea
                            name="prompt"
                            value={form.prompt}
                            onChange={handleChange}
                            placeholder="What is machine learning?"
                            rows={4}
                            className="dark-input resize-none"
                        />
                    </div>

                    {/* model selector */}
                    <div className="flex flex-col gap-2">
                        <label className="text-sm font-medium text-gray-300">
                            Model <span className="text-green-400">*</span>
                        </label>
                        <select
                            name="model_id"
                            value={form.model_id}
                            onChange={handleChange}
                            className="dark-input"
                            style={{ background: '#111' }}
                        >
                            {MODELS.map((m) => (
                                <option key={m.id} value={m.id}>
                                    {m.label}
                                </option>
                            ))}
                        </select>
                    </div>

                    {/* divider */}
                    <div className="border-t border-gray-800" />

                    {/* auto reference toggle */}
                    <Toggle
                        label="Auto-generate Reference"
                        sublabel={autoReference
                            ? "GPT-4o will generate the ideal reference answer"
                            : "Provide your own reference answer below"
                        }
                        enabled={autoReference}
                        onToggle={() => setAutoReference(!autoReference)}
                    />

                    {/* manual reference input */}
                    {!autoReference && (
                        <div className="flex flex-col gap-2 fade-in">
                            <textarea
                                name="reference"
                                value={form.reference}
                                onChange={handleChange}
                                placeholder="The expected or ideal answer..."
                                rows={3}
                                className="dark-input resize-none"
                            />
                        </div>
                    )}

                    {/* auto source toggle */}
                    <Toggle
                        label="Auto-fetch Source Document"
                        sublabel={autoSource
                            ? "Tavily will search the web for relevant source content"
                            : "Provide your own source document below"
                        }
                        enabled={autoSource}
                        onToggle={() => setAutoSource(!autoSource)}
                    />

                    {/* manual source input */}
                    {!autoSource && (
                        <div className="flex flex-col gap-2 fade-in">
                            <textarea
                                name="source"
                                value={form.source}
                                onChange={handleChange}
                                placeholder="Paste the source document the answer should be grounded in..."
                                rows={3}
                                className="dark-input resize-none"
                            />
                        </div>
                    )}

                    {/* submit */}
                    <button
                        onClick={handleSubmit}
                        disabled={loading || !form.prompt}
                        className="gradient-btn py-3 text-sm w-full disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {loading ? 'Running Evaluation...' : 'Run Evaluation'}
                    </button>
                </div>

                {/* loading */}
                {loading && (
                    <div className="mt-8">
                        <LoadingSpinner message="Running evaluation — this may take a moment..." />
                    </div>
                )}

                {/* error */}
                {error && (
                    <div className="mt-8 glass-card p-4 border border-red-500/30">
                        <p className="text-red-400 text-sm">{error}</p>
                    </div>
                )}

                {/* results */}
                {result && (
                    <div className="mt-8 flex flex-col gap-6 fade-in">

                        {/* response */}
                        <div className="glass-card p-6">
                            <h2 className="text-sm font-semibold text-gray-400 mb-3 uppercase tracking-wider">
                                Model Response
                            </h2>
                            <p className="text-gray-200 text-sm leading-relaxed">
                                {result.response}
                            </p>
                        </div>

                        {/* metric scores */}
                        <div className="glass-card p-6">
                            <h2 className="text-sm font-semibold text-gray-400 mb-6 uppercase tracking-wider">
                                Evaluation Scores
                            </h2>
                            <div className="flex flex-col gap-5">
                                {Object.entries(result.metrics).map(([name, metric]) => (
                                    <div key={name} className="flex flex-col gap-2">
                                        <div className="flex justify-between items-center">
                                            <span className="text-sm font-medium text-white">{name}</span>
                                            <span
                                                className="text-sm font-bold"
                                                style={{ color: getScoreColor(metric.score) }}
                                            >
                                                {(metric.score * 100).toFixed(1)}%
                                            </span>
                                        </div>
                                        <div className="score-bar">
                                            <div
                                                className="score-fill"
                                                style={{ width: `${metric.score * 100}%` }}
                                            />
                                        </div>
                                        {metric.passed !== null && (
                                            <span className={`text-xs ${metric.passed ? 'text-green-400' : 'text-red-400'}`}>
                                                {metric.passed ? '✓ Passed' : '✗ Failed'}
                                            </span>
                                        )}
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* metadata */}
                        <div className="glass-card p-4 flex justify-between items-center">
                            <span className="text-xs text-gray-500">
                                Model: <span className="text-gray-300">{result.model}</span>
                            </span>
                            <span className="text-xs text-gray-500">
                                {new Date(result.timestamp).toLocaleString()}
                            </span>
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}

export default Evaluate