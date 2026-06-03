import { useState, useEffect } from 'react'
import { getAllResults } from '../services/api'
import LoadingSpinner from '../components/shared/LoadingSpinner'

const Results = () => {
    const [results, setResults] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)
    const [selected, setSelected] = useState(null)

    useEffect(() => {
        fetchResults()
    }, [])

    const fetchResults = async () => {
        try {
            const data = await getAllResults()
            setResults(data)
        } catch (err) {
            setError('Failed to load results.')
        } finally {
            setLoading(false)
        }
    }

    const getScoreColor = (score) => {
        if (score >= 0.8) return '#22c55e'
        if (score >= 0.5) return '#f59e0b'
        return '#6b7280'
    }

    const formatDate = (timestamp) => {
        return new Date(timestamp).toLocaleString()
    }

    return (
        <div className="relative min-h-screen">

            {/* background orbs */}
            <div className="orb orb-green" style={{ top: '50px', right: '0%' }} />

            <div className="relative z-10 py-12">

                {/* header */}
                <div className="mb-10 flex justify-between items-center">
                    <div>
                        <h1 className="text-4xl font-bold mb-2">
                            Evaluation <span className="gradient-text">History</span>
                        </h1>
                        <p className="text-gray-400">
                            {results.length} evaluation{results.length !== 1 ? 's' : ''} recorded
                        </p>
                    </div>
                    <button
                        onClick={fetchResults}
                        className="glass-card px-4 py-2 text-sm text-gray-300 hover:text-white cursor-pointer"
                    >
                        Refresh
                    </button>
                </div>

                {/* loading */}
                {loading && <LoadingSpinner message="Loading results..." />}

                {/* error */}
                {error && (
                    <div className="glass-card p-4 border border-red-500/30">
                        <p className="text-red-400 text-sm">{error}</p>
                    </div>
                )}

                {/* empty state */}
                {!loading && !error && results.length === 0 && (
                    <div className="glass-card p-12 text-center">
                        <p className="text-gray-400 text-lg mb-2">No evaluations yet</p>
                        <p className="text-gray-500 text-sm">
                            Run your first evaluation to see results here.
                        </p>
                    </div>
                )}

                {/* results list */}
                {!loading && results.length > 0 && (
                    <div className="flex flex-col gap-4">
                        {results.map((result) => (
                            <div
                                key={result.id}
                                className="glass-card p-6 cursor-pointer"
                                onClick={() => setSelected(
                                    selected?.id === result.id ? null : result
                                )}
                            >
                                {/* result header */}
                                <div className="flex justify-between items-start mb-4">
                                    <div className="flex flex-col gap-1">
                                        <p className="text-white font-medium">
                                            {result.prompt}
                                        </p>
                                        <p className="text-xs text-gray-500">
                                            {result.model} · {formatDate(result.timestamp)}
                                        </p>
                                    </div>
                                    <span className="text-xs text-gray-500">
                                        #{result.id}
                                    </span>
                                </div>

                                {/* metric pills */}
                                <div className="flex gap-2 flex-wrap">
                                    {Object.entries(result.metrics).map(([name, metric]) => (
                                        <div
                                            key={name}
                                            className="flex items-center gap-1 px-3 py-1 rounded-full text-xs"
                                            style={{
                                                background: 'rgba(255,255,255,0.05)',
                                                border: `1px solid ${getScoreColor(metric.score)}40`
                                            }}
                                        >
                                            <span className="text-gray-400">{name}</span>
                                            <span
                                                className="font-semibold"
                                                style={{ color: getScoreColor(metric.score) }}
                                            >
                                                {(metric.score * 100).toFixed(1)}%
                                            </span>
                                        </div>
                                    ))}
                                </div>

                                {/* expanded detail */}
                                {selected?.id === result.id && (
                                    <div className="mt-6 pt-6 border-t border-gray-800 fade-in">
                                        <p className="text-sm font-semibold text-gray-400 mb-4 uppercase tracking-wider">
                                            Model Response
                                        </p>
                                        <p className="text-gray-300 text-sm leading-relaxed mb-6">
                                            {result.response}
                                        </p>

                                        <p className="text-sm font-semibold text-gray-400 mb-4 uppercase tracking-wider">
                                            Detailed Scores
                                        </p>
                                        <div className="flex flex-col gap-4">
                                            {Object.entries(result.metrics).map(([name, metric]) => (
                                                <div key={name} className="flex flex-col gap-2">
                                                    <div className="flex justify-between">
                                                        <span className="text-sm text-white">{name}</span>
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
                                                    {metric.details && !metric.details.skipped && (
                                                        <div className="flex gap-4 mt-1">
                                                            {Object.entries(metric.details).map(([k, v]) => (
                                                                <span key={k} className="text-xs text-gray-500">
                                                                    {k}: <span className="text-gray-300">
                                                                        {typeof v === 'number'
                                                                            ? (v * 100).toFixed(1) + '%'
                                                                            : String(v)
                                                                        }
                                                                    </span>
                                                                </span>
                                                            ))}
                                                        </div>
                                                    )}
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    )
}

export default Results