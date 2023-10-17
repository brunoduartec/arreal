import Image from 'next/image'
import { Board } from './components/Board/board'

export default function Home() {
  return (
    <main className="flex min-h-screen flex-row items-left justify-between p-24">
      <Board/>
    </main>
  )
}
