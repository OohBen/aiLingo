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
          <p className="text-[17px] text-gray-200 hidden md:block opacity-100">
            {/*change description here*/}
            aiLingo offers a personal experience, interactive activities, and
            cultural immersion for enhanced language learning.
          </p>
        </div>
      </div>

      <div className="bg-black flex items-center justify-between w-full h-full bg-cover bg-center relative">
        <div
          className="pl-20 md:pl-40 pb-56 md:pb-20 flex gap-5 z-[10] max-w-[750px]"
          style={{ opacity: 0.9 }}
        >
          <div className="flex-grow">
            <h1 className="text-[50px] text-white font-semibold opacity-100">
              Who we are
            </h1>
            <p className="text-[17px] text-gray-200 hidden md:block opacity-100">
              {/*change description here*/}
              aiLingo is an AI-driven language learning platform that provides
              users with customized lessons, instant feedback, and cultural
              immersion for learners of all proficiency levels. This program
              aims to counter traditional language education by embracing a more
              personalized experience, along with interactive and engaging
              lessons, allowing users to reach their linguistic potential. To
              generate income, the program will have an optional paid premium
              membership allowing access to better AI models and extra features
              without diminishing the quality and user experience.
            </p>
          </div>
        </div>
        <div
          className="flex justify-center items-center"
          style={{
            marginRight: "100px",
            marginBottom: "100px",
            marginLeft: "60px",
          }}
        >
          {/* Adjust the margin-right value as needed */}
          <Image
            src="/computer.png" // Replace image here
            alt="Image Description"
            width={250}
            height={250}
          />
        </div>
      </div>
    </main>
  );
}
