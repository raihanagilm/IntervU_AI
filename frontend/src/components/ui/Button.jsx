/**
 * Button Component - Reusable button dengan berbagai varian
 * 
 * Props:
 * - children: Content button
 * - variant: 'primary' | 'secondary' | 'outline'
 * - size: 'sm' | 'md' | 'lg'
 * - onClick: Click handler
 * - disabled: Disable state
 * - className: Additional CSS classes
 * - type: Button type (button, submit, reset)
 */
function Button({
  children,
  variant = 'primary',
  size = 'md',
  onClick,
  disabled = false,
  className = '',
  type = 'button',
  ...props
}) {
  // Base styles untuk semua button
  const baseStyles = 'font-medium rounded-lg transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed'
  
  // Variant styles
  const variantStyles = {
    primary: 'bg-primary-500 hover:bg-primary-600 text-white shadow-sm hover:shadow-md focus:ring-primary-500',
    secondary: 'bg-slate-100 hover:bg-slate-200 text-slate-800 focus:ring-slate-500',
    outline: 'border-2 border-primary-500 text-primary-500 hover:bg-primary-50 focus:ring-primary-500',
  }
  
  // Size styles
  const sizeStyles = {
    sm: 'py-1.5 px-3 text-sm',
    md: 'py-2 px-4 text-base',
    lg: 'py-3 px-6 text-lg',
  }
  
  // Width style - full width on mobile, auto on sm+ screens
  const widthStyle = 'w-full sm:w-auto'
  
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`
        ${baseStyles}
        ${variantStyles[variant]}
        ${sizeStyles[size]}
        ${widthStyle}
        ${className}
      `.trim()}
      {...props}
    >
      {children}
    </button>
  )
}

export default Button
