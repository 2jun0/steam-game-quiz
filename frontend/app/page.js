import { Component } from '@/components/component'
import { getDailyQuizes } from "@/lib/backend-api";

export default async function Home() {
  let quizes = await getDailyQuizes();

  return (
    <Component quizes={quizes}/>
  )
}
