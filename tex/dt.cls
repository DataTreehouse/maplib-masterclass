\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{dt}[2020/07/03]

\RequirePackage{graphicx}
\RequirePackage{tikz}
\RequirePackage{color}
\RequirePackage[utf8]{inputenc}
\RequirePackage{fancyvrb}
\RequirePackage{tcolorbox}
\RequirePackage{fontawesome5}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{beamer}}
\ProcessOptions \relax
\LoadClass[8pt, aspectratio=169]{beamer}

\RequirePackage[familydefault,regular]{Chivo}
\RequirePackage[T1]{fontenc}


\definecolor{dtwhite}{RGB}{254, 254, 251}
\definecolor{dtlightgreen}{RGB}{216, 230, 206}
\definecolor{dtgreen}{RGB}{141, 193, 122}
\definecolor{dtyellow}{RGB}{254, 240, 135}
\definecolor{dtlightorange}{RGB}{254, 240, 135}
\definecolor{dtorange}{RGB}{248, 154, 32}
\definecolor{dtred}{RGB}{241, 103, 103}

\setbeamertemplate{itemize item}{\color{black} \faAngleRight}
\setbeamertemplate{itemize subitem}{\color{black} \faAngleDoubleRight}
\setbeamercolor*{enumerate item}{fg=dtorange}
\setbeamercolor*{description item}{fg=dtorange}
\setbeamercolor*{itemize item}{fg=dtorange}
\setbeamertemplate{footline}[text line]{%
  \parbox{\linewidth}{\vspace*{-8pt} \textcolor{dtred}{\inserttitle \hfill\insertshortauthor \hspace{5pt} \textcopyright{} 2025 Data Treehouse \hfill\insertpagenumber}}}
\setbeamertemplate{navigation symbols}{}

\setbeamertemplate{frametitle}
{
    

	\begin{center}
        \textbf{\textcolor{black}{\normalsize{\insertframetitle}}}

        \vspace{-5pt}

		\begin{tikzpicture}
			\draw[dtgreen, very thick](0,0)--(0.8,0);
		\end{tikzpicture}

	\end{center}
}

\tcbset{
		colframe=dtgreen, 
		sharp corners, 
		colback=dtgreen!8!white,
		width=\textwidth, 
		boxrule=0mm, 
		leftrule=1mm,
        fontupper=\ttfamily,
		left=0.8pt, 
		bottom=1pt, 
		top=1pt
}

\newcommand{\dtgreenit}[1]{\textcolor{dtgreen}{\textit{#1}}}

\newcommand{\tp}[1]{

	

    \begin{center}
        \Large{\textcolor{dtred}{\inserttitle}}

        \vspace{20pt}
        \begin{tikzpicture}
            \node (1) at (0,0) {};
            \node (2) at (9,0) {};

            \draw[dtgreen, thick] (1)--(2);

        \end{tikzpicture}

        
    \end{center}



	\vspace{40pt}

	\normalsize{\textcolor{dtred}{\insertshortauthor}}

    \vspace{5pt}

    {\scriptsize{\textcolor{dtred}{#1}}}
}


\newenvironment{code}{
\setlength\linenumbersep{-.1cm} 
\setcounter{linenumber}{1}
\begin{internallinenumbers}
    \begin{tcolorbox}
            }{
    \end{tcolorbox}
\end{internallinenumbers}
\AfterEndEnvironment{verbatim}{\nolinenumbers}
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
		\draw[dtgreen, very thick](0,0)--(0.7,0);
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
			\draw[dtgreen, very thick](0,0)--(0.7,0);
		\end{tikzpicture}

		\vspace{5pt}

		\Large{\textcolor{dtgreen}{#1}}
	\end{center}
	
}