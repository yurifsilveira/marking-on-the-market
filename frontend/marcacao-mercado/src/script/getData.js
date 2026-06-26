async function getTreasuryDirect() {
    const url = 'http://localhost:8000/investimento/renda_fixa/titulopublico?limit=10000'

    try {
        const response = await fetch(url)

        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`)
        }

        return await response.json()

    } catch (error) {
        console.error(error.message)
        return []
    }
}

export default getTreasuryDirect