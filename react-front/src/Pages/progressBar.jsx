import React from 'react'
export default function ProgressBar({score}) {
   
    
      return (
       <div className="w-full border-gray-300 bg-white border-2 rounded-2xl flex items-center ">
          <div className="bg-green-500 rounded-2xl items-center justify-center min-w-5" style={{width: `${score}%`}}>
          <p className="font-[roboto] text-xs min-w-5">{score} %</p>
        </div>
          </div>
      );
    }
