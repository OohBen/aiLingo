import ContactForm from "../components/contactForm";
import React from "react";
import Navbar from "../components/navbar";
import Image from "next/image";

const Contact = () => {
  return (
    <main>
      <Navbar />
      <div className="w-screen h-screen bg-cover bg-center flex items-center justify-center">
        <div className="h-[60%] w-[80%] relative bg-cover bg-center rounded-xl border border-blue-900">
          <div className="absolute left-20 bottom-10 w-[70%] md:w-[30%]">
            <ContactForm />
          </div>
          <div
            className="flex justify-center items-center"
            style={{
              marginLeft: "400px",
              marginTop: "25px",
            }}
          >
            <Image
              src="/contactImg.png" // Replace image here
              alt="Image Description"
              width={350}
              height={350}
            />
          </div>
        </div>
      </div>
    </main>
  );
};

export default Contact;