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
  
  const [data, setData] = useState([])

  useEffect(() => {
    getTreasuryDirect().then(result => {
      console.log(result)
      setData(result)
    })
  }, [])

  data.forEach(item => {
    console.log(item)
  })
  
  const items = [{
    "title": "LTN - 2025",
    "deadline":"01/01/2025",
    "marketValue": 1000,
    "value":940,
    "median":700,
    "oportunity": 750,
    "img":{img}
  }]

  return (
    <div className="container-fluid w-100"> 
      <Header/>
      <About/>
      <Options/>
      <Section title="Tesouro Direto - LTN" description= "Título público pré-fixado" items={items}/>
      {/* <Card title="LTN - 2025" deadline="01/01/2025" marketValue={1000} median={980} value={970} oportunity={741} img={img}/>
      <Card title="LTN - 2025" deadline="01/01/2025" marketValue={1000} median={980} value={970} oportunity={741} img={img}/> */}
      <Section title="Tesouro Direto - NTN" description= "Título público IPCA+" items={items}/>
    </div>
  )
}

export default App
