import requests
import json
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import threading

class CompactModernConverter:
    def __init__(self):
        self.rates = {}
        self.currency_symbols = {}
        self.last_update = None
        self.load_data()
        self.create_compact_modern_gui()
        self.fetch_live_rates()
        self.schedule_auto_refresh()
    
    def load_data(self):
        """Load offline currency data"""
        try:
            with open('currencyData.txt', 'r') as f:
                lines = f.readlines()
            
            for line in lines:
                try:
                    parts = line.strip().split('\t')
                    if len(parts) >= 2:
                        currency = parts[0]
                        rate = float(parts[1])
                        self.rates[currency] = rate
                except:
                    continue
            
            self.rates['Indian Rupee'] = 1.0
            
        except FileNotFoundError:
            self.rates = {
                'Indian Rupee': 1.0,
                'US Dollar': 0.013588,
                'Euro': 0.011175,
                'British Pound': 0.010200,
                'Japanese Yen': 1.413723
            }
    
    def create_compact_modern_gui(self):
        """Create compact modern interface"""
        self.root = tk.Tk()
        self.root.title("💰 Modern Currency Converter")
        self.root.geometry("600x750")
        self.root.configure(bg='#1a1a2e')
        self.root.resizable(False, False)
        
        # Create main container with modern styling
        main_container = tk.Frame(self.root, bg='#1a1a2e')
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Header with gradient-like effect
        self.create_modern_header(main_container)
        
        # Main converter card
        self.create_converter_card(main_container)
        
        # Result section
        self.create_result_section(main_container)
        
        # Action buttons
        self.create_action_buttons(main_container)
        
        # Footer info  
        self.create_footer_info(main_container)
        
        # Setup initial currencies
        self.setup_initial_currencies()
    
    def create_modern_header(self, parent):
        """Create modern header section"""
        header_frame = tk.Frame(parent, bg='#16213e', relief='flat', bd=0)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Add subtle border
        header_frame.configure(highlightbackground='#0f4c75', highlightthickness=2)
        
        header_inner = tk.Frame(header_frame, bg='#16213e')
        header_inner.pack(fill=tk.X, padx=25, pady=20)
        
        # Title with modern typography
        title = tk.Label(header_inner,
                        text="💰 Currency Converter",
                        font=('Segoe UI', 24, 'bold'),
                        bg='#16213e',
                        fg='#ffffff')
        title.pack()
        
        # Subtitle
        subtitle = tk.Label(header_inner,
                           text="✨ Real-time exchange rates ✨",
                           font=('Segoe UI', 12),
                           bg='#16213e',
                           fg='#3bb78f')
        subtitle.pack(pady=(5, 15))
        
        # Status section with modern indicators
        status_frame = tk.Frame(header_inner, bg='#16213e')
        status_frame.pack()
        
        # Status dot
        self.status_canvas = tk.Canvas(status_frame, width=16, height=16, 
                                      bg='#16213e', highlightthickness=0)
        self.status_canvas.pack(side=tk.LEFT)
        self.status_dot = self.status_canvas.create_oval(2, 2, 14, 14, 
                                                        fill='#ff6b6b', outline='#ff9f9f', width=1)
        
        # Status text
        self.status_label = tk.Label(status_frame,
                                    text="🔄 Loading rates...",
                                    font=('Segoe UI', 11, 'bold'),
                                    bg='#16213e',
                                    fg='#74c0fc')
        self.status_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Animate status dot
        self.animate_status_dot()
    
    def animate_status_dot(self):
        """Animate status indicator"""
        colors = ['#ff6b6b', '#ff9f9f', '#ffd93d', '#ff9f9f']
        color_index = int(datetime.now().second / 2) % len(colors)
        
        try:
            self.status_canvas.itemconfig(self.status_dot, fill=colors[color_index])
        except:
            pass
        
        self.root.after(800, self.animate_status_dot)
    
    def create_converter_card(self, parent):
        """Create main converter card"""
        card_frame = tk.Frame(parent, bg='#0f3460', relief='flat', bd=0)
        card_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Modern border effect
        card_frame.configure(highlightbackground='#3bb78f', highlightthickness=2)
        
        card_inner = tk.Frame(card_frame, bg='#0f3460')
        card_inner.pack(fill=tk.X, padx=25, pady=25)
        
        # Amount section
        amount_frame = tk.Frame(card_inner, bg='#0f3460')
        amount_frame.pack(fill=tk.X, pady=(0, 20))
        
        amount_label = tk.Label(amount_frame,
                               text="💵 Amount",
                               font=('Segoe UI', 14, 'bold'),
                               bg='#0f3460',
                               fg='#74c0fc')
        amount_label.pack(anchor='w', pady=(0, 8))
        
        # Modern amount entry
        entry_frame = tk.Frame(amount_frame, bg='#1e2761', relief='flat')
        entry_frame.pack(fill=tk.X, ipady=10)
        entry_frame.configure(highlightbackground='#74c0fc', highlightthickness=1)
        
        self.amount_var = tk.StringVar(value="1000")
        self.amount_entry = tk.Entry(entry_frame,
                                    textvariable=self.amount_var,
                                    font=('Segoe UI', 16, 'bold'),
                                    bg='#1e2761',
                                    fg='#ffffff',
                                    border=0,
                                    insertbackground='#74c0fc',
                                    justify='center')
        self.amount_entry.pack(fill=tk.X, padx=15, pady=5)
        self.amount_entry.bind('<KeyRelease>', self.on_amount_change)
        
        # Currency selection section
        currency_frame = tk.Frame(card_inner, bg='#0f3460')
        currency_frame.pack(fill=tk.X)
        
        # From currency
        from_frame = tk.Frame(currency_frame, bg='#0f3460')
        from_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        from_label = tk.Label(from_frame,
                             text="📤 From",
                             font=('Segoe UI', 12, 'bold'),
                             bg='#0f3460',
                             fg='#ffd93d')
        from_label.pack(anchor='w', pady=(0, 5))
        
        from_combo_frame = tk.Frame(from_frame, bg='#1e2761', relief='flat')
        from_combo_frame.pack(fill=tk.X, ipady=5)
        from_combo_frame.configure(highlightbackground='#ffd93d', highlightthickness=1)
        
        self.from_var = tk.StringVar()
        self.from_combo = ttk.Combobox(from_combo_frame,
                                      textvariable=self.from_var,
                                      font=('Segoe UI', 11),
                                      state='readonly')
        self.from_combo.pack(fill=tk.X, padx=8, pady=5)
        self.from_combo.bind('<<ComboboxSelected>>', self.on_currency_change)
        
        # Swap button
        swap_frame = tk.Frame(currency_frame, bg='#0f3460')
        swap_frame.pack(side=tk.LEFT, padx=10)
        
        self.swap_btn = tk.Button(swap_frame,
                                 text="🔄",
                                 font=('Segoe UI', 18),
                                 bg='#6c5ce7',
                                 fg='white',
                                 border=0,
                                 width=3,
                                 height=1,
                                 cursor='hand2',
                                 command=self.swap_currencies)
        self.swap_btn.pack(pady=20)
        
        # Hover effects for swap button
        self.swap_btn.bind('<Enter>', lambda e: self.swap_btn.configure(bg='#a29bfe'))
        self.swap_btn.bind('<Leave>', lambda e: self.swap_btn.configure(bg='#6c5ce7'))
        
        # To currency
        to_frame = tk.Frame(currency_frame, bg='#0f3460')
        to_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        
        to_label = tk.Label(to_frame,
                           text="📥 To",
                           font=('Segoe UI', 12, 'bold'),
                           bg='#0f3460',
                           fg='#ff7675')
        to_label.pack(anchor='w', pady=(0, 5))
        
        to_combo_frame = tk.Frame(to_frame, bg='#1e2761', relief='flat')
        to_combo_frame.pack(fill=tk.X, ipady=5)
        to_combo_frame.configure(highlightbackground='#ff7675', highlightthickness=1)
        
        self.to_var = tk.StringVar()
        self.to_combo = ttk.Combobox(to_combo_frame,
                                    textvariable=self.to_var,
                                    font=('Segoe UI', 11),
                                    state='readonly')
        self.to_combo.pack(fill=tk.X, padx=8, pady=5)
        self.to_combo.bind('<<ComboboxSelected>>', self.on_currency_change)
    
    def create_result_section(self, parent):
        """Create result display section"""
        result_frame = tk.Frame(parent, bg='#00b894', relief='flat', bd=0)
        result_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Glowing border effect
        result_frame.configure(highlightbackground='#00cec9', highlightthickness=3)
        
        result_inner = tk.Frame(result_frame, bg='#00b894')
        result_inner.pack(fill=tk.X, padx=25, pady=15)
        
        # Result header
        result_header = tk.Label(result_inner,
                                text="💎 Converted Amount",
                                font=('Segoe UI', 16, 'bold'),
                                bg='#00b894',
                                fg='#ffffff')
        result_header.pack()
        
        # Main result display
        self.result_label = tk.Label(result_inner,
                                    text="Enter amount to convert",
                                    font=('Segoe UI', 28, 'bold'),
                                    bg='#00b894',
                                    fg='#ffffff')
        self.result_label.pack(pady=(10, 0))
        
        # Exchange rate info
        self.rate_info_label = tk.Label(result_inner,
                                       text="",
                                       font=('Segoe UI', 10),
                                       bg='#00b894',
                                       fg='#dff9fb')
        self.rate_info_label.pack(pady=(8, 0))
    
    def create_action_buttons(self, parent):
        """Create action buttons"""
        button_frame = tk.Frame(parent, bg='#1a1a2e')
        button_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Convert button
        self.convert_btn = tk.Button(button_frame,
                                    text="🚀 CONVERT NOW",
                                    font=('Segoe UI', 12, 'bold'),
                                    bg='#e17055',
                                    fg='white',
                                    border=0,
                                    padx=25,
                                    pady=10,
                                    cursor='hand2',
                                    command=self.convert_now)
        self.convert_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        
        # Refresh button
        self.refresh_btn = tk.Button(button_frame,
                                    text="🔄 REFRESH",
                                    font=('Segoe UI', 12, 'bold'),
                                    bg='#0984e3',
                                    fg='white',
                                    border=0,
                                    padx=25,
                                    pady=10,
                                    cursor='hand2',
                                    command=self.manual_refresh)
        self.refresh_btn.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=(10, 0))
        
        # Hover effects
        self.convert_btn.bind('<Enter>', lambda e: self.convert_btn.configure(bg='#fab1a0'))
        self.convert_btn.bind('<Leave>', lambda e: self.convert_btn.configure(bg='#e17055'))
        
        self.refresh_btn.bind('<Enter>', lambda e: self.refresh_btn.configure(bg='#74b9ff'))
        self.refresh_btn.bind('<Leave>', lambda e: self.refresh_btn.configure(bg='#0984e3'))
    
    def create_footer_info(self, parent):
        """Create footer information"""
        footer_frame = tk.Frame(parent, bg='#16213e', relief='flat', bd=0)
        footer_frame.pack(fill=tk.X)
        
        footer_frame.configure(highlightbackground='#0f4c75', highlightthickness=1)
        
        footer_inner = tk.Frame(footer_frame, bg='#16213e')
        footer_inner.pack(fill=tk.X, padx=20, pady=15)
        
        # Feature highlights
        features_text = "🌟 150+ currencies • ⚡ Real-time rates • 🔄 Auto-refresh • 🛡️ Secure"
        
        features_label = tk.Label(footer_inner,
                                 text=features_text,
                                 font=('Segoe UI', 10, 'bold'),
                                 bg='#16213e',
                                 fg='#74c0fc')
        features_label.pack()
        
        # Additional info
        info_text = "Built with modern design principles and advanced algorithms"
        
        info_label = tk.Label(footer_inner,
                             text=info_text,
                             font=('Segoe UI', 9),
                             bg='#16213e',
                             fg='#a0a0a0')
        info_label.pack(pady=(5, 0))
    
    def fetch_live_rates(self):
        """Fetch live rates for ALL available currencies"""
        def fetch():
            try:
                # First, get all supported currencies
                currencies_url = "https://api.exchangerate-api.com/v4/latest/USD"
                response = requests.get(currencies_url, timeout=15)
                response.raise_for_status()
                
                data = response.json()
                rates = data.get('rates', {})
                
                # Comprehensive currency mapping with full names and symbols
                currency_map = {
                    'AED': {'name': 'UAE Dirham', 'symbol': 'د.إ'},
                    'AFN': {'name': 'Afghan Afghani', 'symbol': '؋'},
                    'ALL': {'name': 'Albanian Lek', 'symbol': 'L'},
                    'AMD': {'name': 'Armenian Dram', 'symbol': '֏'},
                    'ANG': {'name': 'Netherlands Antillean Guilder', 'symbol': 'ƒ'},
                    'AOA': {'name': 'Angolan Kwanza', 'symbol': 'Kz'},
                    'ARS': {'name': 'Argentine Peso', 'symbol': '$'},
                    'AUD': {'name': 'Australian Dollar', 'symbol': 'A$'},
                    'AWG': {'name': 'Aruban Florin', 'symbol': 'ƒ'},
                    'AZN': {'name': 'Azerbaijani Manat', 'symbol': '₼'},
                    'BAM': {'name': 'Bosnia-Herzegovina Convertible Mark', 'symbol': 'KM'},
                    'BBD': {'name': 'Barbadian Dollar', 'symbol': '$'},
                    'BDT': {'name': 'Bangladeshi Taka', 'symbol': '৳'},
                    'BGN': {'name': 'Bulgarian Lev', 'symbol': 'лв'},
                    'BHD': {'name': 'Bahraini Dinar', 'symbol': '.د.ب'},
                    'BIF': {'name': 'Burundian Franc', 'symbol': 'FBu'},
                    'BMD': {'name': 'Bermudan Dollar', 'symbol': '$'},
                    'BND': {'name': 'Brunei Dollar', 'symbol': '$'},
                    'BOB': {'name': 'Bolivian Boliviano', 'symbol': 'Bs.'},
                    'BRL': {'name': 'Brazilian Real', 'symbol': 'R$'},
                    'BSD': {'name': 'Bahamian Dollar', 'symbol': '$'},
                    'BTC': {'name': 'Bitcoin', 'symbol': '₿'},
                    'BTN': {'name': 'Bhutanese Ngultrum', 'symbol': 'Nu.'},
                    'BWP': {'name': 'Botswanan Pula', 'symbol': 'P'},
                    'BYN': {'name': 'New Belarusian Ruble', 'symbol': 'Br'},
                    'BZD': {'name': 'Belize Dollar', 'symbol': 'BZ$'},
                    'CAD': {'name': 'Canadian Dollar', 'symbol': 'C$'},
                    'CDF': {'name': 'Congolese Franc', 'symbol': 'FC'},
                    'CHF': {'name': 'Swiss Franc', 'symbol': 'CHF'},
                    'CLP': {'name': 'Chilean Peso', 'symbol': '$'},
                    'CNY': {'name': 'Chinese Yuan', 'symbol': '¥'},
                    'COP': {'name': 'Colombian Peso', 'symbol': '$'},
                    'CRC': {'name': 'Costa Rican Colón', 'symbol': '₡'},
                    'CUC': {'name': 'Cuban Convertible Peso', 'symbol': '$'},
                    'CUP': {'name': 'Cuban Peso', 'symbol': '₱'},
                    'CVE': {'name': 'Cape Verdean Escudo', 'symbol': '$'},
                    'CZK': {'name': 'Czech Republic Koruna', 'symbol': 'Kč'},
                    'DJF': {'name': 'Djiboutian Franc', 'symbol': 'Fdj'},
                    'DKK': {'name': 'Danish Krone', 'symbol': 'kr'},
                    'DOP': {'name': 'Dominican Peso', 'symbol': 'RD$'},
                    'DZD': {'name': 'Algerian Dinar', 'symbol': 'دج'},
                    'EGP': {'name': 'Egyptian Pound', 'symbol': '£'},
                    'ERN': {'name': 'Eritrean Nakfa', 'symbol': 'Nfk'},
                    'ETB': {'name': 'Ethiopian Birr', 'symbol': 'Br'},
                    'EUR': {'name': 'Euro', 'symbol': '€'},
                    'FJD': {'name': 'Fijian Dollar', 'symbol': '$'},
                    'FKP': {'name': 'Falkland Islands Pound', 'symbol': '£'},
                    'GBP': {'name': 'British Pound Sterling', 'symbol': '£'},
                    'GEL': {'name': 'Georgian Lari', 'symbol': '₾'},
                    'GGP': {'name': 'Guernsey Pound', 'symbol': '£'},
                    'GHS': {'name': 'Ghanaian Cedi', 'symbol': '¢'},
                    'GIP': {'name': 'Gibraltar Pound', 'symbol': '£'},
                    'GMD': {'name': 'Gambian Dalasi', 'symbol': 'D'},
                    'GNF': {'name': 'Guinean Franc', 'symbol': 'FG'},
                    'GTQ': {'name': 'Guatemalan Quetzal', 'symbol': 'Q'},
                    'GYD': {'name': 'Guyanaese Dollar', 'symbol': '$'},
                    'HKD': {'name': 'Hong Kong Dollar', 'symbol': 'HK$'},
                    'HNL': {'name': 'Honduran Lempira', 'symbol': 'L'},
                    'HRK': {'name': 'Croatian Kuna', 'symbol': 'kn'},
                    'HTG': {'name': 'Haitian Gourde', 'symbol': 'G'},
                    'HUF': {'name': 'Hungarian Forint', 'symbol': 'Ft'},
                    'IDR': {'name': 'Indonesian Rupiah', 'symbol': 'Rp'},
                    'ILS': {'name': 'Israeli New Sheqel', 'symbol': '₪'},
                    'IMP': {'name': 'Manx pound', 'symbol': '£'},
                    'INR': {'name': 'Indian Rupee', 'symbol': '₹'},
                    'IQD': {'name': 'Iraqi Dinar', 'symbol': 'ع.د'},
                    'IRR': {'name': 'Iranian Rial', 'symbol': '﷼'},
                    'ISK': {'name': 'Icelandic Króna', 'symbol': 'kr'},
                    'JEP': {'name': 'Jersey Pound', 'symbol': '£'},
                    'JMD': {'name': 'Jamaican Dollar', 'symbol': 'J$'},
                    'JOD': {'name': 'Jordanian Dinar', 'symbol': 'JD'},
                    'JPY': {'name': 'Japanese Yen', 'symbol': '¥'},
                    'KES': {'name': 'Kenyan Shilling', 'symbol': 'KSh'},
                    'KGS': {'name': 'Kyrgystani Som', 'symbol': 'лв'},
                    'KHR': {'name': 'Cambodian Riel', 'symbol': '៛'},
                    'KMF': {'name': 'Comorian Franc', 'symbol': 'CF'},
                    'KPW': {'name': 'North Korean Won', 'symbol': '₩'},
                    'KRW': {'name': 'South Korean Won', 'symbol': '₩'},
                    'KWD': {'name': 'Kuwaiti Dinar', 'symbol': 'KD'},
                    'KYD': {'name': 'Cayman Islands Dollar', 'symbol': '$'},
                    'KZT': {'name': 'Kazakhstani Tenge', 'symbol': '₸'},
                    'LAK': {'name': 'Laotian Kip', 'symbol': '₭'},
                    'LBP': {'name': 'Lebanese Pound', 'symbol': '£'},
                    'LKR': {'name': 'Sri Lankan Rupee', 'symbol': '₨'},
                    'LRD': {'name': 'Liberian Dollar', 'symbol': '$'},
                    'LSL': {'name': 'Lesotho Loti', 'symbol': 'M'},
                    'LYD': {'name': 'Libyan Dinar', 'symbol': 'LD'},
                    'MAD': {'name': 'Moroccan Dirham', 'symbol': 'MAD'},
                    'MDL': {'name': 'Moldovan Leu', 'symbol': 'lei'},
                    'MGA': {'name': 'Malagasy Ariary', 'symbol': 'Ar'},
                    'MKD': {'name': 'Macedonian Denar', 'symbol': 'ден'},
                    'MMK': {'name': 'Myanma Kyat', 'symbol': 'K'},
                    'MNT': {'name': 'Mongolian Tugrik', 'symbol': '₮'},
                    'MOP': {'name': 'Macanese Pataca', 'symbol': 'MOP$'},
                    'MRO': {'name': 'Mauritanian Ouguiya', 'symbol': 'UM'},
                    'MRU': {'name': 'Mauritanian Ouguiya', 'symbol': 'UM'},
                    'MUR': {'name': 'Mauritian Rupee', 'symbol': '₨'},
                    'MVR': {'name': 'Maldivian Rufiyaa', 'symbol': 'Rf'},
                    'MWK': {'name': 'Malawian Kwacha', 'symbol': 'MK'},
                    'MXN': {'name': 'Mexican Peso', 'symbol': '$'},
                    'MYR': {'name': 'Malaysian Ringgit', 'symbol': 'RM'},
                    'MZN': {'name': 'Mozambican Metical', 'symbol': 'MT'},
                    'NAD': {'name': 'Namibian Dollar', 'symbol': '$'},
                    'NGN': {'name': 'Nigerian Naira', 'symbol': '₦'},
                    'NIO': {'name': 'Nicaraguan Córdoba', 'symbol': 'C$'},
                    'NOK': {'name': 'Norwegian Krone', 'symbol': 'kr'},
                    'NPR': {'name': 'Nepalese Rupee', 'symbol': '₨'},
                    'NZD': {'name': 'New Zealand Dollar', 'symbol': 'NZ$'},
                    'OMR': {'name': 'Omani Rial', 'symbol': '﷼'},
                    'PAB': {'name': 'Panamanian Balboa', 'symbol': 'B/.'},
                    'PEN': {'name': 'Peruvian Nuevo Sol', 'symbol': 'S/.'},
                    'PGK': {'name': 'Papua New Guinean Kina', 'symbol': 'K'},
                    'PHP': {'name': 'Philippine Peso', 'symbol': '₱'},
                    'PKR': {'name': 'Pakistani Rupee', 'symbol': '₨'},
                    'PLN': {'name': 'Polish Zloty', 'symbol': 'zł'},
                    'PYG': {'name': 'Paraguayan Guarani', 'symbol': 'Gs'},
                    'QAR': {'name': 'Qatari Rial', 'symbol': '﷼'},
                    'RON': {'name': 'Romanian Leu', 'symbol': 'lei'},
                    'RSD': {'name': 'Serbian Dinar', 'symbol': 'Дин.'},
                    'RUB': {'name': 'Russian Ruble', 'symbol': '₽'},
                    'RWF': {'name': 'Rwandan Franc', 'symbol': 'R₣'},
                    'SAR': {'name': 'Saudi Riyal', 'symbol': '﷼'},
                    'SBD': {'name': 'Solomon Islands Dollar', 'symbol': '$'},
                    'SCR': {'name': 'Seychellois Rupee', 'symbol': '₨'},
                    'SDG': {'name': 'Sudanese Pound', 'symbol': 'ج.س.'},
                    'SEK': {'name': 'Swedish Krona', 'symbol': 'kr'},
                    'SGD': {'name': 'Singapore Dollar', 'symbol': 'S$'},
                    'SHP': {'name': 'Saint Helena Pound', 'symbol': '£'},
                    'SLE': {'name': 'Sierra Leonean Leone', 'symbol': 'Le'},
                    'SLL': {'name': 'Sierra Leonean Leone', 'symbol': 'Le'},
                    'SOS': {'name': 'Somali Shilling', 'symbol': 'S'},
                    'SRD': {'name': 'Surinamese Dollar', 'symbol': '$'},
                    'STD': {'name': 'São Tomé and Príncipe Dobra', 'symbol': 'Db'},
                    'STN': {'name': 'São Tomé and Príncipe Dobra', 'symbol': 'Db'},
                    'SVC': {'name': 'Salvadoran Colón', 'symbol': '$'},
                    'SYP': {'name': 'Syrian Pound', 'symbol': '£'},
                    'SZL': {'name': 'Swazi Lilangeni', 'symbol': 'E'},
                    'THB': {'name': 'Thai Baht', 'symbol': '฿'},
                    'TJS': {'name': 'Tajikistani Somoni', 'symbol': 'SM'},
                    'TMT': {'name': 'Turkmenistani Manat', 'symbol': 'T'},
                    'TND': {'name': 'Tunisian Dinar', 'symbol': 'د.ت'},
                    'TOP': {'name': 'Tongan Paʻanga', 'symbol': 'T$'},
                    'TRY': {'name': 'Turkish Lira', 'symbol': '₺'},
                    'TTD': {'name': 'Trinidad and Tobago Dollar', 'symbol': 'TT$'},
                    'TWD': {'name': 'New Taiwan Dollar', 'symbol': 'NT$'},
                    'TZS': {'name': 'Tanzanian Shilling', 'symbol': 'TSh'},
                    'UAH': {'name': 'Ukrainian Hryvnia', 'symbol': '₴'},
                    'UGX': {'name': 'Ugandan Shilling', 'symbol': 'USh'},
                    'USD': {'name': 'US Dollar', 'symbol': '$'},
                    'UYU': {'name': 'Uruguayan Peso', 'symbol': '$U'},
                    'UZS': {'name': 'Uzbekistan Som', 'symbol': 'лв'},
                    'VED': {'name': 'Venezuelan Bolívar', 'symbol': 'Bs'},
                    'VES': {'name': 'Venezuelan Bolívar', 'symbol': 'Bs'},
                    'VND': {'name': 'Vietnamese Dong', 'symbol': '₫'},
                    'VUV': {'name': 'Vanuatu Vatu', 'symbol': 'VT'},
                    'WST': {'name': 'Samoan Tala', 'symbol': 'WS$'},
                    'XAF': {'name': 'CFA Franc BEAC', 'symbol': 'FCFA'},
                    'XAG': {'name': 'Silver (troy ounce)', 'symbol': 'XAG'},
                    'XAU': {'name': 'Gold (troy ounce)', 'symbol': 'XAU'},
                    'XCD': {'name': 'East Caribbean Dollar', 'symbol': '$'},
                    'XDR': {'name': 'Special Drawing Rights', 'symbol': 'SDR'},
                    'XOF': {'name': 'CFA Franc BCEAO', 'symbol': 'CFA'},
                    'XPD': {'name': 'Palladium Ounce', 'symbol': 'XPD'},
                    'XPF': {'name': 'CFP Franc', 'symbol': '₣'},
                    'XPT': {'name': 'Platinum Ounce', 'symbol': 'XPT'},
                    'YER': {'name': 'Yemeni Rial', 'symbol': '﷼'},
                    'ZAR': {'name': 'South African Rand', 'symbol': 'R'},
                    'ZMW': {'name': 'Zambian Kwacha', 'symbol': 'ZK'},
                    'ZWL': {'name': 'Zimbabwean Dollar', 'symbol': 'Z$'},
                }
                
                # Now get rates in terms of USD and convert to INR base
                usd_to_inr = rates.get('INR', 83.0)  # Fallback rate
                
                live_rates = {}
                self.currency_symbols = {}
                
                # Add all available currencies from the API
                for code, usd_rate in rates.items():
                    if code in currency_map and usd_rate > 0:
                        curr_info = currency_map[code]
                        currency_name = curr_info['name']
                        
                        # Convert USD rate to INR base rate
                        if code == 'INR':
                            inr_rate = 1.0
                        elif code == 'USD':
                            inr_rate = 1.0 / usd_to_inr
                        else:
                            inr_rate = usd_rate / usd_to_inr
                        
                        live_rates[currency_name] = inr_rate
                        self.currency_symbols[currency_name] = curr_info['symbol']
                
                # Add any missing important currencies that might not be in rates
                important_missing = {
                    'Indian Rupee': {'rate': 1.0, 'symbol': '₹'}
                }
                
                for curr_name, info in important_missing.items():
                    if curr_name not in live_rates:
                        live_rates[curr_name] = info['rate']
                        self.currency_symbols[curr_name] = info['symbol']
                
                if live_rates:
                    self.rates = live_rates
                    self.last_update = datetime.now()
                    self.root.after(0, self.update_after_fetch)
                    print(f"✅ Fetched {len(live_rates)} live currency rates from {len(rates)} available currencies")
                    
            except Exception as e:
                print(f"❌ Error fetching rates: {e}")
                self.root.after(0, self.update_status_error)
        
        threading.Thread(target=fetch, daemon=True).start()
    
    def update_after_fetch(self):
        """Update UI after fetching rates"""
        currencies = sorted(self.rates.keys())
        
        # Update comboboxes
        current_from = self.from_var.get()
        current_to = self.to_var.get()
        
        self.from_combo['values'] = currencies
        self.to_combo['values'] = currencies
        
        # Restore or set default currencies
        if current_from in currencies:
            self.from_var.set(current_from)
        elif 'Indian Rupee' in currencies:
            self.from_var.set('Indian Rupee')
        elif currencies:
            self.from_var.set(currencies[0])
            
        if current_to in currencies:
            self.to_var.set(current_to)
        elif 'US Dollar' in currencies:
            self.to_var.set('US Dollar')
        elif len(currencies) > 1:
            self.to_var.set(currencies[1])
        elif currencies:
            self.to_var.set(currencies[0])
        
        # Update status
        count = len(currencies)
        time_str = self.last_update.strftime('%H:%M:%S')
        self.status_label.config(text=f"✅ {count} live rates • {time_str}")
        self.status_canvas.itemconfig(self.status_dot, fill='#00b894', outline='#00cec9')
        
        self.convert_now()
    
    def update_status_error(self):
        """Update status on error"""
        self.status_label.config(text="❌ Using offline rates")
        self.status_canvas.itemconfig(self.status_dot, fill='#e74c3c', outline='#ff7675')
    
    def setup_initial_currencies(self):
        """Setup initial currency values"""
        currencies = sorted(self.rates.keys())
        self.from_combo['values'] = currencies
        self.to_combo['values'] = currencies
        
        if currencies:
            self.from_var.set(currencies[0])
            if len(currencies) > 1:
                self.to_var.set(currencies[1])
    
    def schedule_auto_refresh(self):
        """Schedule automatic refresh"""
        def auto_refresh():
            self.fetch_live_rates()
            self.root.after(1800000, auto_refresh)  # 30 minutes
        
        self.root.after(1800000, auto_refresh)
    
    def on_amount_change(self, event=None):
        """Handle amount changes"""
        self.root.after(300, self.convert_now)
    
    def on_currency_change(self, event=None):
        """Handle currency changes"""
        self.convert_now()
    
    def swap_currencies(self):
        """Swap currencies with visual feedback"""
        from_curr = self.from_var.get()
        to_curr = self.to_var.get()
        self.from_var.set(to_curr)
        self.to_var.set(from_curr)
        
        # Visual feedback
        self.swap_btn.configure(bg='#a29bfe')
        self.root.after(200, lambda: self.swap_btn.configure(bg='#6c5ce7'))
        
        self.convert_now()
    
    def manual_refresh(self):
        """Manual refresh with visual feedback"""
        self.refresh_btn.configure(text="⏳ UPDATING...", state='disabled')
        self.status_label.config(text="🔄 Fetching latest rates...")
        self.status_canvas.itemconfig(self.status_dot, fill='#0984e3', outline='#74b9ff')
        
        def restore_button():
            self.refresh_btn.configure(text="🔄 REFRESH", state='normal')
        
        self.root.after(3000, restore_button)
        self.fetch_live_rates()
    
    def convert_now(self):
        """Convert currency with enhanced display"""
        try:
            amount_str = self.amount_var.get().strip()
            if not amount_str:
                self.result_label.config(text="Enter an amount")
                self.rate_info_label.config(text="")
                return
            
            amount = float(amount_str)
            from_currency = self.from_var.get()
            to_currency = self.to_var.get()
            
            if not from_currency or not to_currency:
                self.result_label.config(text="Select currencies")
                self.rate_info_label.config(text="")
                return
            
            if from_currency == to_currency:
                result = amount
            else:
                # Convert via INR
                if from_currency == 'Indian Rupee':
                    inr_amount = amount
                else:
                    inr_amount = amount / self.rates.get(from_currency, 1)
                
                if to_currency == 'Indian Rupee':
                    result = inr_amount
                else:
                    result = inr_amount * self.rates.get(to_currency, 1)
            
            # Format result
            if result >= 1000000:
                formatted = f"{result:,.2f}"
            elif result >= 100:
                formatted = f"{result:,.2f}"
            elif result >= 1:
                formatted = f"{result:.4f}"
            else:
                formatted = f"{result:.6f}".rstrip('0').rstrip('.')
            
            # Get currency symbol
            symbol = self.currency_symbols.get(to_currency, '')
            
            # Update result display
            self.result_label.config(text=f"{symbol}{formatted}")
            
            # Show exchange rate
            if from_currency != to_currency and amount > 0:
                rate = result / amount
                from_symbol = self.currency_symbols.get(from_currency, '')
                rate_text = f"1 {from_symbol} = {rate:.4f} {symbol}"
                self.rate_info_label.config(text=rate_text)
            else:
                self.rate_info_label.config(text="")
                
        except ValueError:
            self.result_label.config(text="❌ Invalid amount")
            self.rate_info_label.config(text="Please enter a valid number")
        except Exception as e:
            self.result_label.config(text="❌ Error")
            self.rate_info_label.config(text="Please try again")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    try:
        app = CompactModernConverter()
        app.run()
    except Exception as e:
        messagebox.showerror("Error", f"Application error: {e}")
        print(f"Error: {e}")
