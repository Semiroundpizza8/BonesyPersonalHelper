import Head from 'next/head'
import styles from '@/styles/Home.module.css'

export default function Home() {
  return (
    <>
      <Head>
        <title>Bonesy Personal Helper</title>
        <meta name="description" content="Bonesy Personal Helper - A Raspberry Pi application with web interface" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main className={styles.main}>
        <div className={styles.container}>
          <h1 className={styles.title}>
            Hello World
          </h1>
          <p className={styles.description}>
            Welcome to the Bonesy Personal Helper frontend
          </p>
        </div>
      </main>
    </>
  )
}