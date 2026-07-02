import type { ReactNode } from 'react';
import { useState, useRef, useEffect } from 'react';
import { ChevronDown } from 'lucide-react';

interface CollapsibleSectionProps {
  title: string;
  subtitle: string;
  children: ReactNode;
  defaultOpen?: boolean;
  actions?: ReactNode;
}

export function CollapsibleSection({ title, subtitle, children, defaultOpen = true, actions }: CollapsibleSectionProps) {
  const [open, setOpen] = useState(defaultOpen);
  const contentRef = useRef<HTMLDivElement>(null);
  const [height, setHeight] = useState<number | undefined>(defaultOpen ? undefined : 0);

  useEffect(() => {
    if (!contentRef.current) return;
    if (open) {
      const scrollH = contentRef.current.scrollHeight;
      setHeight(scrollH);
      const timer = setTimeout(() => setHeight(undefined), 260);
      return () => clearTimeout(timer);
    } else {
      setHeight(contentRef.current.scrollHeight);
      requestAnimationFrame(() => setHeight(0));
    }
  }, [open]);

  return (
    <section className={`surface collapsible-surface ${open ? 'is-open' : 'is-folded'}`}>
      <div className="section-head">
        <button
          className="collapse-toggle"
          onClick={() => setOpen(!open)}
          aria-label={open ? `Collapse ${title}` : `Expand ${title}`}
          title={open ? `Collapse ${title}` : `Expand ${title}`}
        >
          <ChevronDown
            size={16}
            style={{
              transform: open ? 'rotate(0deg)' : 'rotate(-90deg)',
              transition: 'transform 0.25s ease',
            }}
          />
        </button>
        <div style={{ flex: 1 }}>
          <span className="eyebrow">{subtitle}</span>
          <h2>{title}</h2>
        </div>
        {actions}
      </div>
      <div
        ref={contentRef}
        className="collapse-content"
        style={{
          height: height !== undefined ? `${height}px` : 'auto',
          overflow: 'hidden',
          transition: 'height 0.25s ease',
          opacity: open ? 1 : 0,
        }}
      >
        {children}
      </div>
    </section>
  );
}
