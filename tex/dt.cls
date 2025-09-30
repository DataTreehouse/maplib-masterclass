\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{cap}[2020/07/03]

\RequirePackage{graphicx}
\RequirePackage{tikz}
\RequirePackage{color}
\RequirePackage[utf8]{inputenc}
\RequirePackage{fancyvrb}
\RequirePackage{tcolorbox}
\RequirePackage{fontawesome}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{beamer}}
\ProcessOptions \relax
\LoadClass[8pt, aspectratio=169]{beamer}

\RequirePackage[familydefault,regular]{Chivo}
\RequirePackage[T1]{fontenc}


\definecolor{caplightblue}{RGB}{18, 171, 219}
\definecolor{cappurple}{RGB}{43, 10, 62}
\definecolor{capred}{RGB}{255, 48, 76}
\definecolor{caplightgreen}{RGB}{149, 230, 22}
\definecolor{capdkgreen}{RGB}{21, 89, 107}
\definecolor{capaqua}{RGB}{15, 153, 156}
\definecolor{capgray}{RGB}{236, 236, 236}

\setbeamertemplate{itemize item}{\color{black} \faAngleRight}
\setbeamertemplate{itemize subitem}{\color{black} \faAngleDoubleRight}
\setbeamercolor*{enumerate item}{fg=capaqua}
\setbeamercolor*{description item}{fg=capaqua}
\setbeamercolor*{itemize item}{fg=capaqua}
\setbeamertemplate{footline}[text line]{%
  \parbox{\linewidth}{\vspace*{-8pt} \textcolor{teal}{\inserttitle \hfill\insertshortauthor\hfill\insertpagenumber}}}
\setbeamertemplate{navigation symbols}{}

\setbeamertemplate{frametitle}
{
    

	\begin{center}
        \textbf{\textcolor{black}{\normalsize{\insertframetitle}}}

        \vspace{-5pt}

		\begin{tikzpicture}
			\draw[teal, very thick](0,0)--(0.8,0);
		\end{tikzpicture}

	\end{center}
}

\tcbset{
		colframe=teal, 
		sharp corners, 
		colback=teal!3!white,
		width=\textwidth, 
		boxrule=0mm, 
		leftrule=1mm,
        fontupper=\ttfamily,
		left=0.8pt, 
		bottom=1pt, 
		top=1pt
}

\newcommand{\tealit}[1]{\textcolor{teal}{\textit{#1}}}

\newcommand{\tp}[1]{

	

    \begin{center}
        \Large{\textcolor{teal}{\inserttitle}}

        \vspace{20pt}
        \begin{tikzpicture}
            \node (1) at (0,0) {};
            \node (2) at (4,0) {};
            \node (3) at (4.5,0) {\textcolor{teal!50}{\faHeart{}}};
            \node (4) at (5,0) {};
            \node (5) at (9,0) {};

            \draw[teal, thick] (1)--(2);
            \draw[teal, thick] (4)--(5);
        \end{tikzpicture}

        
    \end{center}



	\vspace{40pt}

	\normalsize{\textcolor{teal}{\insertshortauthor}}

    \vspace{5pt}

    {\scriptsize{\textcolor{cappurple}{#1}}}
}

\newenvironment{code}{
    \begin{tcolorbox}
            }{
    \end{tcolorbox}
}

\newcommand{\presentationframev}[2]{
\begin{minipage}{0.30\textwidth}
	\begin{tikzpicture} 
		\begin{scope}
			\clip [rounded corners=1.5cm] (3,0) rectangle coordinate (centerpoint) (6,3); 
			\node [inner sep=0pt] at (centerpoint) {\includegraphics[width=3cm]{#1}}; 
		\end{scope}
	\end{tikzpicture}
\end{minipage}
\hspace{5pt}
\begin{minipage}{0.60\textwidth}
	\begin{tikzpicture}
		\draw[teal, very thick](0,0)--(0.7,0);
	\end{tikzpicture}

	\vspace{5pt}

	\small{\inserttitle}

	\vspace{20pt}

	\small{\insertshortauthor}

	\vspace{5pt}

	\footnotesize{#2}
\end{minipage}
}

\newcommand{\subtitleframe}[1]{

	\begin{center}
		\begin{tikzpicture}
			\draw[teal, very thick](0,0)--(0.7,0);
		\end{tikzpicture}

		\vspace{5pt}

		\Large{\textcolor{teal}{#1}}
	\end{center}
	
}