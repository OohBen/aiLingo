import Image from "next/image";
import Navbar from "./components/navbar";

export default function Home() {
  return (
    <main className="w-screen h-screen relative">
      <Navbar />
      <div
        className="flex items-center w-full h-full bg-cover bg-center relative"
        style={{ backgroundImage: "url(/homebg.jpg)" }}
      >
        <div
          className="pl-20 md:pl-40 pb-56 md:pb-20 flex flex-col gap-5 z-[10] max-w-[750px]"
          style={{ opacity: 0.9 }}
        >
          <span className="text-[55px] font-semibold text-transparent bg-clip-text bg-gradient-to-r from-blue-300 to-blue-600">
            {" "}
            Language Learning
          </span>
          <h1 className="text-[50px] text-white font-semibold opacity-100">
            made easy
          </h1>
          <p className="text-gray-200 hidden md:block opacity-100">
            {/*change description here*/}
            aiLingo offers a personal experience, interactive activities, and
            cultural immersion for enhanced language learning.
          </p>
        </div>
      </div>
    </main>
  );
}
