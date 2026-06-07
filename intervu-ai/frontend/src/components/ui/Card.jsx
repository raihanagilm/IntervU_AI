import React from 'react'

const Card = ({ children, className = '', ...props }) => {
  return (
    <div
      className={`bg-white rounded-xl shadow-sm border border-slate-100 p-4 sm:p-6 transition-layout ${className}`}
      {...props}
    >
      {children}
    </div>
  )
}

export default Card
