import React from 'react'


export default function Score  ({score = 0}) {
  
  return (
    <div className = "border-gray-300 bg-white border-2 rounded-2xl flex max-w-xs items-center justify-center">
      <h1 className="font-[roboto] text-3xl m-3">{score} %</h1>
      <img className = "h-10 m-3" src="https://cdn-icons-png.flaticon.com/512/5610/5610944.png" alt="icone check"/>
    </div>
  );
}