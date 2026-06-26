import { useState, useEffect } from 'react'
import './App.css'
import Header from './components/headers/Header'
import About from './components/market-marking/about'
import Options from './components/market-marking/Option'
import Section from './components/market-marking/Section'
import Card from './components/Card'
import img from './assets/icone-tesouro.png'
import openLink from './assets/open.png'
import getTreasuryDirect from './script/getData'

function App() {
  
  const [itemsNTN, setItemsNTN] = useState([])
  const [itemsLTN, setItemsLTN] = useState([])

  useEffect(() => {
    getTreasuryDirect().then(items => {
      const types = Object.groupBy(items, item => `${item.tipo}`)
      const NTN = Object.entries(
          Object.groupBy(types["NTN"], item => item['vencimento']))
          .map(([deadline, row]) => {
              const orderedRows = [...row].sort(
                (a, b) => new Date(b.data) - new Date(a.data)
              );
              const value = 0
              const median = orderedRows.reverse(row => row["data"]).slice(0,18).reduce((acc, row) => acc + Number(row["pu_compra_manha"]),0)/18
              const marketValue = orderedRows.reverse(row => row["data"])[0]["pu_compra_manha"]
              const oportunity = value ?  value - median : - marketValue - median

              return {
                  "title": `NTN - ${deadline.split('-')[0]}`,
                  "deadline": deadline,
                  "median":Number(median.toFixed(2)),
                  "marketValue":Number(marketValue.toFixed(2)),
                  "value":0,
                  "oportunity": Number(oportunity.toFixed(2)),
                  "img":{img}
              }
          })

      const LTN = Object.entries(
          Object.groupBy(types["LTN"], item => item['vencimento']))
          .map(([deadline, row]) => {
              const value = 0
              const median = row.reverse(row => row["data"]).slice(0,18).reduce((acc, row) => acc + Number(row["pu_compra_manha"]),0)/18
              const marketValue = row.reverse(row => row["data"])[0]["pu_compra_manha"]
              const oportunity = value ? median - value : median - marketValue
              return {
                  "title": `LTN - ${deadline.split('-')[0]}`,
                  "deadline": deadline,
                  "median":Number(median.toFixed(2)),
                  "marketValue":Number(marketValue.toFixed(2)),
                  "value":0,
                  "oportunity": Number(oportunity.toFixed(2)),
                  "img":{img}
              }
          })

      setItemsNTN(NTN.sort((a, b) => a.deadline.localeCompare(b.deadline)))
      setItemsLTN(LTN.sort((a, b) => a.deadline.localeCompare(b.deadline)))
    })
  }, [])

  return (
    <div className="container-fluid w-100"> 
      <Header/>
      <About/>
      <Options/>
      <Section title="Tesouro Direto - LTN" description= "Título público pré-fixado" items={itemsLTN}/>
      {/* <Card title="LTN - 2025" deadline="01/01/2025" marketValue={1000} median={980} value={970} oportunity={741} img={img}/>
      <Card title="LTN - 2025" deadline="01/01/2025" marketValue={1000} median={980} value={970} oportunity={741} img={img}/> */}
      <Section title="Tesouro Direto - NTN" description= "Título público IPCA+" items={itemsNTN}/>
    </div>
  )
}

export default App
