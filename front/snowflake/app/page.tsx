import Image from 'next/image'
import { Block } from './block'

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      Ola
      <Block
      name = {"Banana"}
      shouldRender = {true}
      />
    </main>
  )
}
