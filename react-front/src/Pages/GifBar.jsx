import React from 'react'

export default function GifBar({image, prediction}) {
  
  
  return (
    <div className="relative max-w-xl mx-auto">
    <img className="h-64 w-full object-cover rounded-3xl" src={image} alt="prediction"/>
    <div className="absolute inset-0  opacity-20 rounded-md"></div>
    <div className="absolute inset-0 flex items-end justify-center p-6">
        <h2 className="text-white text-3xl font-bold">{prediction}</h2>
    </div>
      </div>
  )

}
