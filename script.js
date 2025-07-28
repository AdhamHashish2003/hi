async function fetchPrice(asset) {
    const url = `https://api.coingecko.com/api/v3/simple/price?ids=${asset}&vs_currencies=usd`;
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error('Failed to fetch price');
    }
    const data = await response.json();
    return data[asset].usd;
}

document.getElementById('investment-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const asset = document.getElementById('asset').value.trim().toLowerCase();
    const price = parseFloat(document.getElementById('price').value);
    const units = parseFloat(document.getElementById('units').value);
    try {
        const currentPrice = await fetchPrice(asset);
        const currentValue = currentPrice * units;
        const profitLoss = currentValue - (price * units);
        document.getElementById('current-price').textContent = currentPrice.toFixed(2);
        document.getElementById('current-value').textContent = currentValue.toFixed(2);
        document.getElementById('profit-loss').textContent = profitLoss.toFixed(2);
        document.getElementById('result').classList.remove('hidden');
    } catch (err) {
        alert(err.message);
    }
});
