/**
 * Card Component - Reusable card container
 * 
 * Props:
 * - children: Content card
 * - className: Additional CSS classes
 * - hoverable: Enable hover effect
 * - onClick: Click handler (jika clickable)
 */
function Card({
  children,
  className = '',
  hoverable = false,
  onClick,
  ...props
}) {
  // Base styles untuk semua cards
  const baseStyles = 'bg-white rounded-xl shadow-sm border border-slate-100 transition-all duration-300'
  
  // Padding adaptif - lebih kecil di mobile, lebih besar di desktop
  const paddingStyles = 'p-4 sm:p-6'
  
  // Hover styles jika hoverable
  const hoverStyles = hoverable 
    ? 'hover:shadow-md hover:border-primary-200 cursor-pointer' 
    : ''
  
  return (
    <div
      onClick={onClick}
      className={`
        ${baseStyles}
        ${paddingStyles}
        ${hoverStyles}
        ${className}
      `.trim()}
      {...props}
    >
      {children}
    </div>
  )
}

export default Card
