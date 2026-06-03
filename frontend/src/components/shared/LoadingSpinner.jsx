const LoadingSpinner = ({ message = "Processing..." }) => {
    return (
        <div className="flex flex-col items-center justify-center py-20 gap-4">
            <div className="spinner"></div>
            <p className="text-gray-400 text-sm">{message}</p>
        </div>
    )
}

export default LoadingSpinner