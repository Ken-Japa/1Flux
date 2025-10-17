from bs4 import BeautifulSoup

def gerar_quick_view_section(posts_json):
    """
    Gera seção Quick View em HTML
    SEM chamar IA adicional
    """
    
    quick_html = """
    <div class="quick-view-section" style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px;
        margin: 30px 0;
        border-radius: 12px;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    ">
        <h2 style="color: white; border: none; margin-top: 0; font-size: 2em;">
            ⚡ Quick View - Versão Rápida
        </h2>
        <p style="opacity: 0.9; font-size: 1.1em; margin-bottom: 30px;">
            Um resumo dos posts dessa semana. Role para baixo para ver a estratégia completa.
        </p>
    """
    
    
    for i, post in enumerate(posts_json, 1):
        # Extrai legenda principal (primeiros 300 chars)
        legenda_principal = post.get('legenda_principal', '')
        variacoes = post.get('variacoes_legenda', [])
        
        # Se legenda principal < 300 chars E tem variações, adiciona primeira
        if len(legenda_principal) < 300 and variacoes:
            legenda_completa = f"{legenda_principal}\n\n {variacoes[0]} \n{variacoes[1]}"
        else:
            legenda_completa = legenda_principal
        
        # Trunca se passar de 500 chars
        legenda_truncada = legenda_completa[:500] + '...' if len(legenda_completa) > 500 else legenda_completa
        legenda_curta = strip_html(legenda_truncada)
        
        # Pega até 8 hashtags
        hashtags = ' '.join(post['hashtags'][:8])
        
        quick_html += f"""
        <div style="
            background: white;
            color: #333;
            padding: 25px;
            margin: 20px 20px;
            margin-bottom: 30px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <h3 style="margin: 0; color: #667eea; font-size: 1.3em;">
                    Post {i}: {post['titulo']}
                </h3>
                <a href="#post-{i}" style="color: #667eea; text-decoration: underline; font-size: 0.95em; margin-left: 10px;">Ver detalhes completos</a>
            </div>
            
            <p style="margin: 10px 0; color: #666; font-size: 0.95em;">
                📅 <strong>{post.get('horario_de_postagem', 'Definir')}</strong>
            </p>
            
            <!-- Legenda copyable -->
           <div style="
             background: #f0f0f0;
            padding: 12px 16px;
            border-radius: 8px;  /* Menos arredondado = melhor pra texto longo */
            font-size: 0.85em;
            font-weight: bold;
            color: #666;
            margin: 10px 0;
            line-height: 1.5;  /* Espaçamento entre linhas */
            display: inline-block;  /* Só ocupa o espaço necessário */
            max-width: 100%;  /* Mas respeita container */
        ">
                    {post['sugestao_formato']}

            </div>
            
            <div style="margin: 20px 20px;">
                <label style="
                    display: block;
                    font-weight: bold;
                    margin-bottom: 8px;
                    color: #667eea;
                    font-size: 0.9em;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                ">
                    📝 Legenda:
                </label>
                <textarea readonly onclick="this.select()" style="
                    width: 100%;
                    min-height: 120px;
                    padding: 15px;
                    border: 2px solid #e0e0e0;
                    border-radius: 6px;
                    font-family: inherit;
                    font-size: 0.95em;
                    line-height: 1.6;
                    resize: vertical;
                    cursor: pointer;
                    transition: border-color 0.3s;
                " onfocus="this.style.borderColor='#667eea'">{legenda_curta}</textarea>
            </div>
            
            <!-- Hashtags copyable -->
            <div style="margin: 20px 20px;">
                <label style="
                    display: block;
                    font-weight: bold;
                    margin-bottom: 8px;
                    color: #667eea;
                    font-size: 0.9em;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                ">
                    #️⃣ Hashtags:
                </label>
                <input 
                    type="text" 
                    readonly 
                    onclick="this.select()"
                    value="{hashtags}"
                    style="
                        width: 100%;
                        padding: 12px 15px;
                        border: 2px solid #e0e0e0;
                        border-radius: 6px;
                        font-family: inherit;
                        cursor: pointer;
                        font-size: 0.9em;
                    "
                    onfocus="this.style.borderColor='#667eea'"
                />
            </div>
            
            <!-- CTA -->
            <div style="
                background: #f8f9ff;
                padding: 15px;
                border-left: 4px solid #667eea;
                border-radius: 4px;
                margin-top: 15px;
            ">
                <strong style="color: #667eea; font-size: 1.05em;">💬 CTA:</strong> 
                <span style="color: #333;">{post['cta_individual']}</span>
            </div>
            
            <div style="
                background: #f8f9ff;
                padding: 15px;
                border-left: 4px solid #667eea;
                border-radius: 4px;
                margin-top: 15px;
            ">
            <strong style="color: #667eea; font-size: 1.05em;">Indicador Principal:</strong> 
                <span style="color: #333;">{post.get('indicador_principal', 'N/A')}</span>
            </div>
            
        </div>
        """
    
    quick_html += """
        <div style="
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid rgba(255,255,255,0.3);
        ">
            <p style="font-size: 1.2em; margin-bottom: 10px; font-weight: bold;">
                ⬇️ Role para baixo para ver:
            </p>
            <div style="
                display: flex;
                justify-content: center;
                gap: 20px;
                flex-wrap: wrap;
                font-size: 0.95em;
                opacity: 0.9;
            ">
                <span>✨ Estratégia completa</span>
                <span>🎨 Roteiros de Reels/Carrosséis</span>
                <span>📊 Métricas e A/B tests</span>
                <span>💬 Scripts de resposta</span>
            </div>
        </div>
    </div>
    """
    
    return quick_html

def strip_html(text):
    """
    Remove tags HTML e retorna texto puro.
    """
    if not text:
        return ''
    soup = BeautifulSoup(text, 'html.parser')
    return soup.get_text().strip()