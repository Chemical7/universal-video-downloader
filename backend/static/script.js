document.addEventListener('DOMContentLoaded', () => {
    const urlInput = document.getElementById('urlInput');
    const searchBtn = document.getElementById('searchBtn');
    const resultSection = document.getElementById('resultSection');
    const errorMsg = document.getElementById('errorMsg');
    const loader = document.querySelector('.loader');
    const btnText = document.querySelector('.btn-text');

    // Result Elements
    const thumbnail = document.getElementById('thumbnail');
    const videoTitle = document.getElementById('videoTitle');
    const videoDuration = document.getElementById('videoDuration');
    const formatSelect = document.getElementById('formatSelect');
    const downloadBtn = document.getElementById('downloadBtn');

    // State
    let currentVideoInfo = null;

    searchBtn.addEventListener('click', handleSearch);
    urlInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSearch();
    });

    downloadBtn.addEventListener('click', handleDownload);

    function setLoading(isLoading) {
        if (isLoading) {
            searchBtn.disabled = true;
            loader.classList.remove('hidden');
            btnText.classList.add('hidden');
        } else {
            searchBtn.disabled = false;
            loader.classList.add('hidden');
            btnText.classList.remove('hidden');
        }
    }

    async function handleSearch() {
        const url = urlInput.value.trim();
        if (!url) return;

        setLoading(true);
        errorMsg.classList.add('hidden');
        resultSection.classList.add('hidden');

        try {
            const response = await fetch(`/api/info?url=${encodeURIComponent(url)}`);
            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.detail || 'Failed to fetch video info');
            }

            const data = await response.json();
            currentVideoInfo = data;
            displayResults(data);
        } catch (err) {
            errorMsg.textContent = err.message;
            errorMsg.classList.remove('hidden');
        } finally {
            setLoading(false);
        }
    }

    function displayResults(data) {
        thumbnail.src = data.thumbnail;
        videoTitle.textContent = data.title;
        videoDuration.textContent = formatDuration(data.duration);

        // Populate formats
        formatSelect.innerHTML = '';

        // Simple heuristic: unique resolutions, prioritise higher
        const uniqueResolutions = new Map();

        data.formats.forEach(format => {
            const label = format.resolution || (format.ext + ' (' + format.format_id + ')');
            // If we haven't seen this resolution or this one is better (not implemented yet, just taking first for now)
            if (!uniqueResolutions.has(label)) {
                uniqueResolutions.set(label, format.format_id);
                const option = document.createElement('option');
                option.value = format.format_id;
                option.textContent = `${label} [${format.ext}]`;
                formatSelect.appendChild(option);
            }
        });

        resultSection.classList.remove('hidden');
    }

    async function handleDownload() {
        if (!currentVideoInfo) return;

        const formatId = formatSelect.value;
        // For now, we redirect to the direct URL if the backend merely echoes it
        // Or we trigger a download from the backend

        try {
            const response = await fetch(`/api/download?url=${encodeURIComponent(currentVideoInfo.original_url)}&format_id=${formatId}`);
            if (!response.ok) throw new Error('Download failed to start');

            const data = await response.json();
            if (data.direct_url) {
                // Create a temporary link to download
                window.open(data.direct_url, '_blank');
            }
        } catch (err) {
            alert('Error: ' + err.message);
        }
    }

    function formatDuration(seconds) {
        if (!seconds) return 'N/A';
        const m = Math.floor(seconds / 60);
        const s = seconds % 60;
        return `${m}:${s.toString().padStart(2, '0')}`;
    }
});
